document.addEventListener('DOMContentLoaded', function() {
    // Satu listener utama untuk menangani semua klik (Event Delegation)
    document.addEventListener('click', function(e) {
        
        // 1. Handle Klik Tombol VIEW (Lihat)
        const viewBtn = e.target.closest('.view-class-btn');
        if (viewBtn) {
            e.preventDefault();
            const id = viewBtn.getAttribute('data-id');
            openViewModal(id);
        }

        // 2. Handle Klik Tombol EDIT (Pensil)
        const editBtn = e.target.closest('.edit-class-btn');
        if (editBtn) {
            const id = editBtn.getAttribute('data-id');
            openEditModal(id);
        }
    });

    // Handle Form Submit untuk Update
    const editForm = document.getElementById('editClassForm');
    if (editForm) {
        editForm.addEventListener('submit', function(e) {
            e.preventDefault();
            submitUpdateForm();
        });
    }
});

// --- FUNGSI HELPER ---

async function openViewModal(id) {
    try {
        const response = await fetch(`/get-class-details/${id}/`);
        const data = await response.json();
        // ... (Tambahkan logika render modal view kamu di sini)
        document.getElementById("classModal").classList.remove("hidden");
    } catch (err) {
        console.error("Error:", err);
    }
}

async function openEditModal(id) {
    try {
        const response = await fetch(`/get-class-details/${id}/`);
        if (!response.ok) throw new Error('Gagal');
        const data = await response.json();
        
        document.getElementById('editClassId').value = id;
        document.getElementById('editNamaKelas').value = data.judul_kelas;
        document.getElementById('editSiswa').value = data.siswa ? data.siswa.map(s => s.nama).join(', ') : '';
        document.getElementById('editModul').value = data.modul ? data.modul.map(m => m.judul).join(', ') : '';
        
        document.getElementById('editClassModal').classList.remove('hidden');
    } catch (err) {
        alert("Terjadi kesalahan.");
    }
}

async function submitUpdateForm() {
    const id = document.getElementById('editClassId').value;
    const data = {
        judul_kelas: document.getElementById('editNamaKelas').value,
        // ... sesuaikan dengan field yang ingin di-update
    };

    try {
        const response = await fetch(`/get-class-details/${id}/update/`, { // Sesuaikan URL update-mu
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]')?.value // Pastikan ada CSRF token di form
            },
            body: JSON.stringify(data)
        });
        if(response.ok) location.reload();
        else alert("Gagal update data!");
    } catch (err) {
        console.error(err);
    }
}

// Fungsi global agar bisa dipanggil dari tombol di HTML
function closeEditModal() {
    document.getElementById('editClassModal').classList.add('hidden');
}

function closeModal() {
    document.getElementById('classModal').classList.add('hidden');
}