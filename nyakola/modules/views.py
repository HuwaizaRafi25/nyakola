from django.shortcuts import render
from django.core.paginator import Paginator
from db_connection import modules_collection # Pastikan ini import-nya benar

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