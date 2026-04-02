document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const btnSubmit = document.getElementById('btnSubmit');
    
    // Status pengecekan ketersediaan di Database (Dari Server)
    let isUsernameTaken = false;
    let isEmailTaken = false;

    // 1. Selector Semua Elemen Input
    const getInputs = () => ({
        fullname: document.getElementById('fullname'),
        username: document.getElementById('username'),
        gender: document.getElementById('gender'),
        email: document.getElementById('email'),
        password: document.getElementById('password'),
        
        // Elemen Pesan Error Merah
        usernameError: document.getElementById('username-taken-error'),
        emailError: document.getElementById('emailError'),
        
        // Elemen Checklist Username
        reqUserLength: document.getElementById('req-user-length') 
    });

    // 2. Selector Elemen Checklist Password
    const getRequirements = () => ({
        reqLength: document.getElementById('req-length'),
        reqNameEmail: document.getElementById('req-name-email'),
        reqSymbol: document.getElementById('req-symbol'),
        strengthText: document.getElementById('strength-text')
    });

    // 3. Fungsi Update Visual Checklist (Mengubah ✕ Merah menjadi ✓ Hijau)
    function updateRequirementUI(el, isValid) {
        if (!el) return;
        const icon = el.querySelector('.status-icon');
        if (isValid) {
            el.classList.remove('text-red-400');
            el.classList.add('text-green-600');
            if (icon) icon.innerText = '✓';
        } else {
            el.classList.remove('text-green-600');
            el.classList.add('text-red-400');
            if (icon) icon.innerText = '✕';
        }
    }

    // 4. Fungsi Cek ke Server (Django -> MongoDB)
    async function checkAvailability(field, value, errorEl) {
        // Jangan cek ke server jika kurang dari 3 karakter untuk menghemat beban server
        if (value.length < 3) {
            if (errorEl) {
                errorEl.classList.add('hidden');
                errorEl.classList.remove('flex');
            }
            return false; 
        }

        try {
            // Memanggil alamat di urls.py Django
            const response = await fetch(`/check-availability/?${field}=${value}`);
            const data = await response.json();
            
            if (data.is_taken) {
                // Jika sudah ada yang pakai, munculkan pesan error merah
                if (errorEl) {
                    errorEl.classList.remove('hidden');
                    errorEl.classList.add('flex'); // Pakai flex agar icon dan teks sejajar
                }
                return true; 
            } else {
                // Jika aman, sembunyikan pesan error
                if (errorEl) {
                    errorEl.classList.add('hidden');
                    errorEl.classList.remove('flex');
                }
                return false; 
            }
        } catch (error) {
            console.error(`Gagal mengecek ${field}:`, error);
            return false;
        }
    }

    // 5. Fungsi Validasi Utama (Dijalankan setiap kali user mengetik)
    async function validate() {
        const inputs = getInputs();
        const reqs = getRequirements();
        
        // Cek agar tidak error jika elemen belum dimuat (Safety check)
        if (!inputs.fullname || !inputs.password) return;

        // Ambil dan bersihkan nilai input
        const data = {
            fullname: inputs.fullname.value.trim().toLowerCase(),
            username: inputs.username.value.trim(),
            email: inputs.email.value.trim().toLowerCase(),
            password: inputs.password.value
        };

        // --- Logika Checklist Username ---
        const isUsernameLongEnough = data.username.length >= 4;
        updateRequirementUI(inputs.reqUserLength, isUsernameLongEnough);

        // --- Logika Checklist Password ---
        const isLongEnough = data.password.length >= 8;
        const hasNumberOrSymbol = /[\d!@#$%^&*(),.?":{}|<>]/.test(data.password);
        const emailPrefix = data.email.split('@')[0];
        
        // Password tidak boleh mengandung nama lengkap atau nama sebelum @ di email
        const containsSensitive = (data.fullname && data.password.toLowerCase().includes(data.fullname)) || 
                                  (emailPrefix && data.password.toLowerCase().includes(emailPrefix));
        
        const isPasswordSecure = data.password !== "" && !containsSensitive;

        // Update UI untuk syarat password
        updateRequirementUI(reqs.reqLength, isLongEnough);
        updateRequirementUI(reqs.reqSymbol, hasNumberOrSymbol);
        updateRequirementUI(reqs.reqNameEmail, isPasswordSecure);

        // Update Text Kekuatan Password (Weak / Strong)
        if (isLongEnough && hasNumberOrSymbol && isPasswordSecure) {
            reqs.strengthText.innerText = "Strong";
            reqs.strengthText.parentElement.className = "font-bold mt-1 text-green-600";
        } else {
            reqs.strengthText.innerText = "Weak";
            reqs.strengthText.parentElement.className = "font-bold mt-1 text-red-400";
        }

        // --- Logika Tombol Submit Aktif / Mati ---
        const isAllFilled = data.fullname !== "" && 
                            data.username.length >= 4 && // Syarat username min 4 karakter
                            inputs.gender.value !== "" && 
                            data.email.includes('@');

        const isPasswordValid = isLongEnough && hasNumberOrSymbol && isPasswordSecure;

        // Tombol Aktif JIKA: 
        // 1. Semua terisi benar
        // 2. Password kuat
        // 3. Username belum ada di server
        // 4. Email belum ada di server
        if (isAllFilled && isPasswordValid && !isUsernameTaken && !isEmailTaken) {
            btnSubmit.disabled = false;
            btnSubmit.style.backgroundColor = "#606C38"; // Warna Hijau Olive
            btnSubmit.style.cursor = "pointer";
            btnSubmit.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            btnSubmit.disabled = true;
            btnSubmit.style.backgroundColor = "#9CA3AF"; // Warna Abu-abu mati
            btnSubmit.style.cursor = "not-allowed";
            btnSubmit.classList.add('opacity-50', 'cursor-not-allowed');
        }
    }

    // 6. Event Listener: Menangkap ketikan user
    let typingTimer;
    form.addEventListener('input', (e) => {
        const inputs = getInputs();

        // Pengecekan Database HANYA untuk Username dan Email
        // Menggunakan "debounce" (menunggu 0.5 detik setelah user berhenti mengetik)
        // Agar tidak me-request ke server setiap satu huruf diketik
        if (e.target.id === 'username' || e.target.id === 'email') {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(async () => {
                if (e.target.id === 'username') {
                    isUsernameTaken = await checkAvailability('username', e.target.value.trim(), inputs.usernameError);
                } else if (e.target.id === 'email') {
                    isEmailTaken = await checkAvailability('email', e.target.value.trim(), inputs.emailError);
                }
                validate(); // Panggil validasi lagi setelah dapat jawaban dari server
            }, 500); 
        }

        // Jalankan validasi untuk SEMUA perubahan form (seperti password, nama, gender)
        if (['INPUT', 'SELECT'].includes(e.target.tagName)) {
            validate();
        }
    });

    // 7. Pengamanan Lapisan Terakhir saat Tombol Daftar Ditekan
    form.addEventListener('submit', function(e) {
        if (btnSubmit.disabled) {
            e.preventDefault(); // Batalkan pengiriman form
            alert("Harap lengkapi semua persyaratan dan pastikan data belum terdaftar!");
        }
    });
});
