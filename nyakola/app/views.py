from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from db_connection import users_collection
from django.db import models
from django.http import JsonResponse
from django.contrib.auth.models import User
import re

def index(request):
    return render(request, 'index.html')

def register(request):
    if request.method == 'POST':
        email = request.POST.get('email').lower()
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        role = request.POST.get('role')

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
            'password': hashed_password,
            'role' : role
        }
        
        users_collection.insert_one(user_data)
        messages.success(request, 'Registrasi berhasil! Silakan login.')
        return redirect('login')

    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('pw', '').strip()

        user_account = users_collection.find_one({"username": username})

        if user_account and check_password(password, user_account['password']):
            request.session['user_id'] = str(user_account['_id'])
            request.session['profile_pic'] = user_account.get('profile_pic')
            request.session['username'] = user_account['username']
            request.session['email'] = user_account['email']
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
        # Cek ke MongoDB apakah username sudah ada
        user_exists = users_collection.find_one({
            'username': re.compile(f'^{re.escape(username)}$', re.IGNORECASE)
        })
        is_taken = True if user_exists else False
        
    elif email:
        # Cek ke MongoDB apakah email sudah ada
        email_exists = users_collection.find_one({
            'email': re.compile(f'^{re.escape(email)}$', re.IGNORECASE)
        })
        is_taken = True if email_exists else False

    return JsonResponse({'is_taken': is_taken})

