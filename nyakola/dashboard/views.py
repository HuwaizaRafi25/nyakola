from django.shortcuts import render, redirect
from django.contrib import messages
from db_connection import users_collection

def dashboard(request):
    # user_id = request.session.get('user_id')
    # if not user_id:
    #     messages.error(request, 'Anda harus login terlebih dahulu!')
    #     return redirect('login')

    # user_account = users_collection.find_one({"_id": user_id})
    # if not user_account:
    #     messages.error(request, 'Akun tidak ditemukan!')
    #     return redirect('login')

    # context = {
    #     'username': user_account['username'],
    #     'email': user_account['email'],
    #     'fullname': user_account['fullname'],
    # }
    role = request.session.get('role')
    
    if role == 'admin':
        base_template = 'admin_base.html'
    elif role == 'student':
        base_template = 'student_base.html'
    else:
        base_template = '404.html'        # atau 'base.html'

    context = {
        'parent_base': base_template,     # ← ini yang penting
    }
    
    return render(request, 'dashboard.html', context)
    
def settings(request):
    return render(request, 'settings.html')