from django.shortcuts import render
from bson import ObjectId
from django.core.paginator import Paginator
from db_connection import modules_collection, learning_progress

def manage_modul(request):
    # 1. Ambil data langsung dari MongoDB
    # .find() mengembalikan cursor, ubah jadi list
    data_list = list(modules_collection.find({})) 
    
    # 2. Paginator-nya Django bisa dipakai untuk List (bukan cuma QuerySet!)
    paginator = Paginator(data_list, 5) # 5 item per halaman
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'query': request.GET.get('q', '')
    }
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
    
    quiz_history = learning_progress.find_one({"id_user": ObjectId(request.user.id), "id_module": module_id})
    
    context = {
        'quiz_history': quiz_history,
        'module': module_data,
        'quiz_id': quiz_id # Dilempar untuk dipakai fetch data ujian nanti
    }

    return render(request, 'quiz_prep_page.html', context)