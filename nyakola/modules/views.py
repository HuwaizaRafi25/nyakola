from django.shortcuts import render
from bson import ObjectId
from django.core.paginator import Paginator
from db_connection import modules_collection, learning_progress
from django.utils.dateparse import parse_datetime

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

    quiz_attempts = []
    if learning_doc:
        if quiz_id == "final" or quiz_id == "QF-SD":
            quiz_akhir = learning_doc.get('progres_quiz_akhir', {})
            quiz_attempts = quiz_akhir.get('attempts', [])
        else:
            for progress_sub in learning_doc.get('progres_quiz_sub_modul', []):
                if progress_sub.get('id_quiz') == quiz_id:
                    quiz_attempts = progress_sub.get('attempts', [])
                    break
                
        for a in quiz_attempts: a['date'] = parse_datetime(a['date'])
        
    context = {
        'module': module_data,
        'quiz': selected_quiz, 
        'attempts': sorted(quiz_attempts, key=lambda x: x['attempt_no'], reverse=True),
        'quiz_id': quiz_id,
    }
    
    return render(request, 'quiz_prep_page.html', context) 