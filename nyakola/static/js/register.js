document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registerForm');
    const btnSubmit = document.getElementById('btnSubmit');
    
    let isUsernameTaken = false;
    let isEmailTaken = false;

    const getInputs = () => ({
        fullname: document.getElementById('fullname'),
        username: document.getElementById('username'),
        gender: document.getElementById('gender'),
        email: document.getElementById('email'),
        password: document.getElementById('password'),
        emailError: document.getElementById('emailError'),
        reqUserLength: document.getElementById('req-user-length'),
        topNotification: document.getElementById('top-notification') 
    });

    const getRequirements = () => ({
        reqLength: document.getElementById('req-length'),
        reqNameEmail: document.getElementById('req-name-email'),
        reqSymbol: document.getElementById('req-symbol'),
        strengthText: document.getElementById('strength-text')
    });

    function updateRequirementUI(el, isValid) {
        if (!el) return;
        const icon = el.querySelector('.status-icon');
        if (isValid) {
            el.classList.replace('text-red-400', 'text-green-600');
            if (icon) icon.innerText = '✓';
        } else {
            el.classList.replace('text-green-600', 'text-red-400');
            if (icon) icon.innerText = '✕';
        }
    }

    async function checkAvailability(field, value) {
        if (value.length < 3) return false; 
        try {
            const response = await fetch(`/ajax/check-availability/?${field}=${encodeURIComponent(value)}`);
            const data = await response.json();
            return data.is_taken; 
        } catch (error) {
            console.error("Gagal cek ketersediaan:", error);
            return false;
        }
    }

    async function validate() {
        const inputs = getInputs();
        const reqs = getRequirements();
        
        const data = {
            fullname: inputs.fullname.value.trim().toLowerCase(),
            username: inputs.username.value.trim(),
            email: inputs.email.value.trim().toLowerCase(),
            password: inputs.password.value
        };

        // 1. Validasi Syarat
        const isUsernameLongEnough = data.username.length >= 4;
        const isPasswordLong = data.password.length >= 8;
        const hasSymbol = /[\d!@#$%^&*(),.?":{}|<>]/.test(data.password);
        
        const emailPrefix = data.email.split('@')[0];
        const containsSensitive = (data.fullname && data.password.toLowerCase().includes(data.fullname)) || 
                                 (emailPrefix && data.password.toLowerCase().includes(emailPrefix));
        
        const isPasswordSecure = data.password !== "" && !containsSensitive;

        // 2. Update UI Checklist
        updateRequirementUI(inputs.reqUserLength, isUsernameLongEnough);
        updateRequirementUI(reqs.reqLength, isPasswordLong);
        updateRequirementUI(reqs.reqSymbol, hasSymbol);
        updateRequirementUI(reqs.reqNameEmail, isPasswordSecure);

        // 3. Update Teks "Lemah" ke "Kuat"
        const isPasswordValid = isPasswordLong && hasSymbol && isPasswordSecure;
        
        if (isPasswordValid) {
            reqs.strengthText.innerText = "Kuat";
            reqs.strengthText.parentElement.className = "font-bold mt-1 text-green-600";
        } else {
            reqs.strengthText.innerText = "Lemah";
            reqs.strengthText.parentElement.className = "font-bold mt-1 text-red-400";
        }

        // 4. Kunci Tombol Submit
        const isAllFilled = data.fullname && isUsernameLongEnough && inputs.gender.value && data.email.includes('@');

        if (isAllFilled && isPasswordValid && !isUsernameTaken && !isEmailTaken) {
            btnSubmit.disabled = false;
            btnSubmit.style.backgroundColor = "#606C38";
            btnSubmit.classList.remove('opacity-50', 'cursor-not-allowed');
        } else {
            btnSubmit.disabled = true;
            btnSubmit.style.backgroundColor = "#9CA3AF";
            btnSubmit.classList.add('opacity-50', 'cursor-not-allowed');
        }
    }

    let typingTimer;
    form.addEventListener('input', async (e) => {
        // --- PENAMBAHAN FITUR LOWERCASE REAL-TIME ---
        if (e.target.id === 'username' || e.target.id === 'email') {
            e.target.value = e.target.value.toLowerCase();
        }
        // --------------------------------------------

        const inputs = getInputs();
        const val = e.target.value.trim();

        if (e.target.id === 'username') {
            clearTimeout(typingTimer);
            typingTimer = setTimeout(async () => {
                isUsernameTaken = await checkAvailability('username', val);
                if (isUsernameTaken) {
                    inputs.topNotification.classList.remove('hidden');
                    inputs.topNotification.innerHTML = `
                        <div class="flex items-center p-4 mb-4 text-sm text-blue-800 border border-blue-200 rounded-lg bg-blue-50">
                            <span class="font-medium mr-2">Info:</span> Username "${val}" sudah terdaftar. Gunakan yang lain!
                        </div>`;
                    e.target.classList.add('border-red-500', 'text-red-500');
                } else {
                    inputs.topNotification.classList.add('hidden');
                    e.target.classList.remove('border-red-500', 'text-red-500');
                }
                validate();
            }, 500);
        }

        if (e.target.id === 'email') {
            isEmailTaken = await checkAvailability('email', val);
            if (inputs.emailError) {
                inputs.emailError.classList.toggle('hidden', !isEmailTaken);
            }
            validate();
        }

        validate();
    });
});
