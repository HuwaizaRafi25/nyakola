from django.shortcuts import render, get_object_or_404, redirect
from db_connection import modules_collection
from django.http import JsonResponse
from bson import ObjectId
from django.core.paginator import Paginator
from db_connection import modules_collection, learning_progress
from django.utils.dateparse import parse_datetime
from .models import Module


def save_module_content(request, module_id):
    if request.method == 'POST':
        id_bab = request.POST.get('id_bab')
        judul_bab = request.POST.get('judul_bab')
        konten = request.POST.get('konten')

        # Pastikan tidak ada referensi ke class 'Bab' yang tidak terdefinisi
        result = modules_collection.update_one(
            {
                "id_module": module_id, 
                "sub_modul.bab.id_bab": id_bab
            },
            {
                "$set": {
                    "sub_modul.$[sub].bab.$[b].judul_bab": judul_bab,
                    "sub_modul.$[sub].bab.$[b].konten": konten
                }
            },
            array_filters=[
                {"sub.bab.id_bab": id_bab},
                {"b.id_bab": id_bab}
            ]
        )

        if result.modified_count > 0:
            print(f"Berhasil update bab {id_bab} di module {module_id}")
        else:
            print("Peringatan: Tidak ada data yang diubah atau ID tidak cocok.")

        return redirect('module_editor', module_id=module_id)


def manage_modules(request):
    # --- 1. PINTU UNTUK PROSES SIMPAN (CREATE) ---
    # Logika ini hanya jalan kalau kamu klik tombol "Simpan Modul" di modal
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        category = request.POST.get('category')
        
        # Simpan ke MongoDB Atlas
        modules_collection.insert_one({
            "judul_modul": title,
            "author": author,
            "category": category,
            "sub_modul": [] # Wajib ada agar saat dibuka detailnya tidak error
        })
        # Setelah simpan, segarkan halaman agar data baru muncul di tabel
        return redirect('manage_modules')

    # --- 2. LOGIKA TAMPIL DATA (READ) ---
    # Bagian ini tetap dipertahankan supaya tabel tidak kosong
    query = request.GET.get('q', '')
    if query:
        data_list = list(modules_collection.find({"judul_modul": {"$regex": query, "$options": "i"}}))
    else:
        data_list = list(modules_collection.find({})) 
    
    # Paginator (Biar datanya rapi 5 baris per halaman)
    paginator = Paginator(data_list, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': query
    }
    # Kembalikan ke template manajemen modul
    return render(request, 'manage_module.html', context)

def showModule(request, module_id, chapter_id):
    # Ambil data modul berdasarkan module_id dan chapter_id
    module_data = modules_collection.find_one({"id_module": module_id})

    target_bab = None
    for sub in module_data.get("sub_modul", []):
        for bab in sub.get("bab", []):
            if bab.get("id_bab") == chapter_id:
                target_bab = bab
                break    

    if not module_data:
        return render(request, '404.html', status=404)  # Halaman 404 jika data tidak ditemukan
    
    context = {
        'module': module_data,
        'chapter': target_bab
    }
    return render(request, 'module_page.html', context)

def quizPrep(request, module_id, quiz_id):
    module_data = modules_collection.find_one({"id_module": module_id})

    if not module_data:
        return render(request, '404.html', status=404)

    selected_quiz = None
    
    if quiz_id == "final" or quiz_id == "QF-SD": 
        selected_quiz = module_data.get('quiz_akhir_modul')
        if selected_quiz and 'passing_grade' not in selected_quiz:
            selected_quiz['passing_grade'] = 75 
    else:
        for sub in module_data.get('sub_modul', []):
            for bab in sub.get('bab', []):
                quiz = bab.get('quiz_submodul')
                if quiz and quiz.get('id_quiz') == quiz_id:
                    selected_quiz = quiz
                    break
            if selected_quiz: break

    if not selected_quiz:
        return render(request, '404.html', {"message": "Quiz tidak ditemukan"}, status=404)

    learning_doc = learning_progress.find_one({
        "id_user": request.session.get('user_id'), 
        "id_modul": module_id
    })

def module_editor(request, module_id):
    # 1. Ambil data modul dari MongoDB berdasarkan module_id
    module_data = modules_collection.find_one({"id_module": module_id})
    
    if not module_data:
        return render(request, '404.html', status=404)

    context = {
        'module': module_data,
        'module_id': module_id,
    }
    
    # 2. Arahkan ke template khusus editor
    return render(request, 'module_editor.html', context) 