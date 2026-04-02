from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from db_connection import users_collection
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import User
import os

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not all([username, email, fullname, gender, password]):
            print(request, 'Semua field wajib diisi!')
            return redirect('register')
        
        if len(password) < 8:
            print(request, 'Password minimal 8 karakter!')
            return redirect('register')

        if users_collection.find_one({'$or': [{'username': username}, {'email': email}]}):
            print(request, 'Username atau Email sudah digunakan!')
            return redirect('register')

        hashed_password = make_password(password)
        user_data = {
            'username': username,
            'email': email,
            'fullname': fullname,
            'gender': gender,
            'password': hashed_password
        }
        
        users_collection.insert_one(user_data)
        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('login')

    return render(request, 'register.html')

def check_username(request):
    username = request.GET.get('username', None)
    # Cek ke database (case-insensitive)
    exists = User.objects.filter(username__iexact=username).exists()
    return JsonResponse({'is_taken': exists})

def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('pw', '').strip()

        user_account = users_collection.find_one({"username": username})

        if user_account and check_password(password, user_account['password']):
            request.session['user_id'] = str(user_account['_id'])
            request.session['username'] = user_account['username']
            request.session['role'] = user_account.get('role')
            
            return redirect('dashboard') 
        else:
            messages.error(request, 'Username atau Password salah!')
            return redirect('login') 

    else:
        if 'username' in request.session:
            return redirect('dashboard')
            
        return render(request, 'login.html')
    
def logout(request):
    request.session.flush()
    messages.success(request, 'Anda berhasil logout!')
    return redirect('login')

def check_availability(request):
    username = request.GET.get('username', None)
    email = request.GET.get('email', None)
    
    is_taken = False

    if username:
        # Pengecekan username secara case-insensitive
        is_taken = User.objects.filter(username__iexact=username).exists()
    elif email:
        # Pengecekan email secara case-insensitive
        is_taken = User.objects.filter(email__iexact=email).exists()

    return JsonResponse({'is_taken': is_taken})

