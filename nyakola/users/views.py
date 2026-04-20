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
    for user in users:
        user['id'] = str(user['_id'])
    return render(request, 'manage_user.html', {'users': users})

def add_user(request):
    if request.method == 'POST':
        user_data = {
            'username': request.POST.get('username'),
            'full_name': request.POST.get('fullname'),  # FIX INI
            'email': request.POST.get('email'),
            'role': 'siswa',  # FIX: jangan ambil dari form (nggak ada)
        }

        users_collection.insert_one(user_data)
        messages.success(request, "User berhasil ditambahkan!")
    
    return redirect('user_list') 


def update_user(request, id):
    if request.method == 'POST':
        update_data = {
            '$set': {
                'username': request.POST.get('username'),
                'full_name': request.POST.get('fullname'),
                'email': request.POST.get('email'),
            }
        }
        users_collection.update_one({'_id': ObjectId(id)}, update_data)
        messages.success(request, "User berhasil diupdate!")
        return redirect('user_list')

from bson.errors import InvalidId

def delete_user(request, id):
    try:
        if request.method == "POST":
            users_collection.delete_one({'_id': ObjectId(id)})
            messages.success(request, "User berhasil dihapus!")
    except InvalidId:
        messages.error(request, "ID tidak valid!")
    return redirect('user_list')

def manage_users(request):
    users = list(users_collection.find())
    
    # DEBUG: Cek di terminal/console apakah datanya ada isinya
    print("DEBUG - Data User dari MongoDB:", users)
    
    return render(request, 'manage_user.html', {'semua_user': users})
