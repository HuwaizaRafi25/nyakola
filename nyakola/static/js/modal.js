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
        const response = await fetch(`/classes/get-class-details/${id}/`); 
        const data = await response.json();
        
        // Logika render modal view (sesuaikan ID dengan HTML modal detail kamu)
        const modal = document.getElementById("classModal");
        if (modal) {
            // Contoh pengisian data sederhana
            // document.getElementById('viewNamaKelas').innerText = data.judul_kelas;
            modal.classList.remove("hidden");
        }
    } catch (err) {
        console.error("Error:", err);
    }
}

async function openEditModal(id) {
    try {
        // Tambahkan /classes/ sesuai path Django kamu
        const response = await fetch(`/classes/get-class-details/${id}/`); 
        
        if (!response.ok) throw new Error('Gagal mengambil data');
        const data = await response.json();
        
        // Ambil elemen input/textarea
        const idInput = document.getElementById('editClassId');
        const namaInput = document.getElementById('editNamaKelas');
        const siswaTextarea = document.getElementById('editSiswa');
        const modulTextarea = document.getElementById('editModul');
        
        if (idInput && namaInput) {
            idInput.value = id;
            namaInput.value = data.judul_kelas || '';
            
            // Update: Penanganan data Siswa (Map jika array, tampilkan string jika sudah string)
            if (siswaTextarea) {
                siswaTextarea.value = Array.isArray(data.siswa) 
                    ? data.siswa.map(s => s.nama || s).join(', ') 
                    : (data.siswa || '');
            }

            // Update: Penanganan data Modul
            if (modulTextarea) {
                modulTextarea.value = Array.isArray(data.modul) 
                    ? data.modul.map(m => m.judul || m).join(', ') 
                    : (data.modul || '');
            }
            
            document.getElementById('editClassModal').classList.remove('hidden');
        } else {
            console.error("Elemen input modal tidak lengkap di HTML!");
        }
        
    } catch (err) {
        console.error("Detail Error:", err);
        alert("Terjadi kesalahan saat memuat data.");
    }
}

async function submitUpdateForm() {
    const id = document.getElementById('editClassId').value;
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]')?.value;

    const data = {
        judul_kelas: document.getElementById('editNamaKelas').value,
        siswa: document.getElementById('editSiswa').value,
        modul: document.getElementById('editModul').value
    };

    try {
        // Sesuaikan URL update dengan urls.py kamu
        const response = await fetch(`/classes/get-class-details/${id}/update/`, { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken
            },
            body: JSON.stringify(data)
        });

        if (response.ok) {
            alert("Data berhasil diperbarui!");
            location.reload();
        } else {
            const errorRes = await response.json();
            alert("Gagal update: " + (errorRes.message || "Terjadi kesalahan"));
        }
    } catch (err) {
        console.error("Error saat update:", err);
        alert("Terjadi kesalahan koneksi.");
    }
}

// Fungsi global untuk tutup modal
function closeEditModal() {
    document.getElementById('editClassModal').classList.add('hidden');
}

function closeModal() {
    document.getElementById('classModal').classList.add('hidden');
}