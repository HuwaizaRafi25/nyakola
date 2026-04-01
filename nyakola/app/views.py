from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from db_connection import users_collection
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

def login(request):
    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        password = request.POST.get('pw', '').strip()

        user_account = users_collection.find_one({"username": username})

        if user_account and check_password(password, user_account['password']):
            full_name = user_account.get('fullname', username)
            # return HttpResponse(f"<h1>Login Successful! Welcome, {full_name}</h1>")
            print(make_password('kepoamatsih'))
            return render(request, 'index.html')
        else:
            messages.error(request, 'Username atau Password salah!')
            # return redirect('login')
            print("yahaha salah")

    else:
        return render(request, 'login.html')