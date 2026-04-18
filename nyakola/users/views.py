from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from db_connection import users_collection
from bson import ObjectId
from django.http import JsonResponse
import re

def index(request):
    return render(request, 'index.html')

def user_list(request):
    users = list(users_collection.find())
    return render(request, 'manage_user.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        user_data = {
            'username': request.POST.get('username'),
            'fullname': request.POST.get('full_name'),
            'email': request.POST.get('email'),
            'role': request.POST.get('role'),
        }
        users_collection.insert_one(user_data)
        messages.success(request, "User berhasil ditambahkan!")
        return redirect('user_list')
    return render(request, 'user_form.html')

def update_user(request, id):
    if request.method == 'POST':
        update_data = {
            '$set': {
                'username': request.POST.get('username'),
                'full_name': request.POST.get('full_name'),
                'email': request.POST.get('email'),
                'role': request.POST.get('role'),
            }
        }
        users_collection.update_one({'_id': ObjectId(id)}, update_data)
        return redirect('user_list')
    
    user = users_collection.find_one({'_id': ObjectId(id)})
    return render(request, 'user_form.html', {'user': user})

def delete_user(request, id):
    users_collection.delete_one({'_id': ObjectId(id)})
    messages.success(request, "User berhasil dihapus!")
    return redirect('user_list')

def manage_users(request):
    users = list(users_collection.find())
    
    # DEBUG: Cek di terminal/console apakah datanya ada isinya
    print("DEBUG - Data User dari MongoDB:", users)
    
    return render(request, 'manage_user.html', {'semua_user': users})
