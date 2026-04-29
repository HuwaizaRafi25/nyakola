document.addEventListener('DOMContentLoaded', () => {
    const usernameInput = document.getElementById('username'); // Pastikan di modal admin ID-nya ini
    const btnSubmit = document.getElementById('btnSubmit'); // Tombol simpan di modal
    
    let isUsernameTaken = false;
    let typingTimer;

    // Fungsi cek ke server (Sama dengan kodinganmu)
    async function checkAvailability(field, value) {
        if (value.length < 3) return false;
        try {
            const response = await fetch(`/ajax/check-availability/?${field}=${encodeURIComponent(value)}`);
            const data = await response.json();
            return data.is_taken;
        } catch (error) {
            return false;
        }
    }

    // Fungsi validasi sederhana untuk Admin
    function validateAdminForm() {
        const usernameVal = usernameInput ? usernameInput.value.trim() : "";
        
        // Cek syarat minimal: username > 3 huruf & tidak sedang dipakai
        const isValid = usernameVal.length >= 4 && !isUsernameTaken;

        if (btnSubmit) {
            if (isValid) {
                btnSubmit.disabled = false;
                btnSubmit.style.backgroundColor = "#606C38"; // Warna Olive Nyakola
                btnSubmit.classList.remove('opacity-50', 'cursor-not-allowed');
            } else {
                btnSubmit.disabled = true;
                btnSubmit.style.backgroundColor = "#9CA3AF"; // Warna Abu-abu
                btnSubmit.classList.add('opacity-50', 'cursor-not-allowed');
            }
        }
    }

    // Jalankan listener jika input username ada
    if (usernameInput) {
        usernameInput.addEventListener('input', (e) => {
            const val = e.target.value.toLowerCase();
            e.target.value = val; // Force lowercase

            clearTimeout(typingTimer);
            typingTimer = setTimeout(async () => {
                isUsernameTaken = await checkAvailability('username', val);
                
                if (isUsernameTaken) {
                    e.target.classList.add('border-red-500', 'text-red-600', 'bg-red-50');
                    // Tambahkan pesan error kecil jika mau
                } else {
                    e.target.classList.remove('border-red-500', 'text-red-600', 'bg-red-50');
                }
                validateAdminForm();
            }, 500);
        });
    }
});