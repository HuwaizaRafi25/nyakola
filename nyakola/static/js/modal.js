document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById("classModal");
    
    document.addEventListener('click', function(e) {
        const btn = e.target.closest('.view-class-btn');
        if (btn) {
            e.preventDefault();
            e.stopPropagation();

            const classId = btn.getAttribute('data-id');
            
            // Log untuk memastikan ID yang diambil benar (bukan tulisan {class_Id})
            console.log("Mengambil data untuk Class ID:", classId);

            // Pastikan URL mengarah ke endpoint yang benar di urls.py
            fetch(`/classes/get-class-details/${classId}/`)
                .then(response => {
                    // Cek jika server tidak memberikan respon 200 OK
                    if (!response.ok) {
                        throw new Error(`Server merespon dengan status: ${response.status}`);
                    }
                    return response.json();
                })
                .then(data => {
                    // Debugging: Lihat isi data di console browser
                    console.log("Data diterima dari server:", data);

                    // 1. Update Judul dan Mentor (Sesuai kode kamu)
                    document.getElementById('modalTitle').innerText = data.judul_kelas || "Tanpa Nama";
                    document.getElementById('modalMentor').innerText = data.nama_mentor || "-";
                    
                    // 2. Render Daftar Siswa
                    const listSiswa = document.getElementById('modalStudents');
                    listSiswa.innerHTML = ""; 

                    if (data.siswa && data.siswa.length > 0) {
                        data.siswa.forEach(s => {
                            const li = document.createElement('li');
                            li.className = "flex items-center gap-3 text-sm text-[#283618] font-medium p-2 bg-white rounded-lg shadow-sm";
                            li.innerHTML = ` 
                                <div class="flex items-center gap-2"> 
                                    <span class="w-2 h-2 bg-[#606C38] rounded-full"></span> ${s.nama}`;
                            </div>
                            <span class="text-[10px] text-gray-400 font-normal">ID: ${s.id.substring(0,5)}...</span>
                        `;
                        listSiswa.appendChild(li);
                        });
                    } else {
                        listSiswa.innerHTML = "<li class='text-gray-400 italic text-center py-2'>Belum ada siswa</li>";
                    }

                    // 3. Render Daftar Modul (Sesuai arahan gabungan)
                    const listModul = document.getElementById('modalModules');
                    if (listModul) {
                        listModul.innerHTML = "";
                        // Menggunakan data.modul (pastikan di views.py kamu kuncinya bernama 'modul')
                        if (data.modul && data.modul.length > 0) {
                            data.modul.forEach(m => {
                                const li = document.createElement('li');
                                li.className = "text-xs p-2 bg-white rounded-lg border border-gray-100 shadow-sm text-gray-700 font-bold flex items-center gap-2";
                                li.innerHTML = `📖 ${m.judul}`;
                                listModul.appendChild(li);
                            });
                        } else {
                            listModul.innerHTML = "<li class='text-gray-400 italic text-center py-2 text-xs'>Belum ada modul</li>";
                        }
                    }

                    // Tampilkan Modal
                    modal.classList.remove("hidden");
                })
                .catch(err => {
                    console.error("Detail Error:", err);
                    alert("Gagal memuat data. Pastikan URL di urls.py sudah benar dan server aktif.");
                });
        }
    });
});

function closeModal() {
    const modal = document.getElementById("classModal");
    if (modal) {
        modal.classList.add("hidden");
    }
}

// Gunakan cara ini agar klik selalu terdeteksi, meskipun elemen baru muncul
document.addEventListener('click', function(event) {
    // Mengecek apakah yang diklik adalah tombol pensil atau ikon di dalamnya
    const btn = event.target.closest('.edit-class-btn');
    
    if (btn) {
        const id = btn.getAttribute('data-id');
        console.log("Tombol diklik, ID: " + id); // Untuk testing di console
        
        // Ambil data detail kelas
        fetch(`/classes/get-class-details/${id}/`)
            .then(res => res.json())
            .then(data => {
                // Masukkan data ke modal
                document.getElementById('editClassId').value = id;
                document.getElementById('editNamaKelas').value = data.judul_kelas;
                document.getElementById('editSiswa').value = data.siswa ? data.siswa.join(', ') : '';
                document.getElementById('editModul').value = data.modul ? data.modul.map(m => m.judul).join(', ') : '';
                
                // Tampilkan modal
                document.getElementById('editClassModal').classList.remove('hidden');
            })
            .catch(err => console.error("Error fetching data:", err));
    }
    function closeEditModal() {
    document.getElementById('editModal').style.display = 'none';
}
});
    fetch(`/classes/update/${id}/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': '{{ csrf_token }}' // Django CSRF Token
        },
        body: JSON.stringify(data)
    }).then(response => {
        if(response.ok) location.reload(); // Refresh setelah sukses
        else alert("Gagal update data!");
    });
 