from django.shortcuts import render, redirect
from django.contrib import messages
from db_connection import users_collection
from bson.objectid import ObjectId

def dashboard(request):
    # Logika dashboard kamu sudah oke, pastikan role terambil benar
    role = request.session.get('role')
    base_template = 'admin_base.html' if role == 'admin' else 'student_base.html'
    
    context = {'parent_base': base_template}
    return render(request, 'dashboard.html', context)
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
    # 1. Ambil user_id dari session (Pastikan user sudah login)
    user_id = request.session.get('user_id')
    if not user_id:
        messages.error(request, 'Silakan login terlebih dahulu')
        return redirect('login')

    # 2. Cari data user di MongoDB
    # Jika user_id kamu string, perlu diubah ke ObjectId
    user_data = users_collection.find_one({"_id": ObjectId(user_id)})

    if request.method == 'POST':
        # 3. Logika Update Data (Saat tombol Save dipencet)
        new_fullname = request.POST.get('fullname')
        new_phone = request.POST.get('phone')
        
        # Update ke MongoDB
        users_collection.update_one(
            {"_id": ObjectId(user_id)},
            {"$set": {
                "fullname": new_fullname,
                "phone": new_phone,
                # Tambahkan field lain sesuai form kamu
            }}
        )
        
        messages.success(request, 'Profil berhasil diperbarui!')
        return redirect('settings') # Refresh halaman biar data terbaru muncul

    # 4. Kirim data user ke HTML (Tampilan awal/Show mode)
    context = {
        'user': user_data,
        'parent_base': 'admin_base.html' if request.session.get('role') == 'admin' else 'student_base.html'
    }
    return render(request, 'settings.html')