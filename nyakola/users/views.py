from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.views.generic import ListView, UpdateView, DetailView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.contrib import messages # Memastikan ini ada
from django.db.models import Q


# Halaman utama manajemen user
class UserSinglePageView(ListView):
    model = User
    template_name = 'manage_user.html'
    context_object_name = 'semua_user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreationForm() 
        return context

    def post(self, request, *args, **kwargs):
        # --- TAMBAHAN LOGIKA VALIDASI CUSTOM ---
        
        # 1. Ambil data dari request (Urutan: username, phone, gender, birth_date, fullname, email, password)
        u_name = request.POST.get('username')
        f_name = request.POST.get('fullname')
        email = request.POST.get('email')
        pwd = request.POST.get('password')
        # phone, gender, birth_date bisa ditangkap di sini jika ada model Profile tambahan
        
        error_exists = False

        # 2. Cek Username Ganda
        if User.objects.filter(username__iexact=u_name).exists():
            messages.error(request, "Username sudah terdaftar.", extra_tags='username_error')
            error_exists = True

        # 3. Cek Fullname Ganda (diperiksa ke first_name)
        if User.objects.filter(first_name__iexact=f_name).exists():
            messages.error(request, "Nama lengkap sudah terdaftar.", extra_tags='fullname_error')
            error_exists = True

        # 4. Cek Email Ganda
        if User.objects.filter(email__iexact=email).exists():
            messages.error(request, "Email sudah terdaftar.", extra_tags='email_error')
            error_exists = True

        # 5. Jika ada error, hentikan proses dan kembali ke halaman
        if error_exists:
            return self.get(request, *args, **kwargs)

        # --- JIKA LOLOS VALIDASI, GUNAKAN LOGIKA BAWAAN KAMU ---
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.first_name = f_name # Menyimpan fullname ke first_name
            user.email = email
            user.save()
            messages.success(request, "Siswa berhasil ditambahkan!")
            return redirect('manage_users')
            
        return self.get(request, *args, **kwargs)

# Endpoint khusus untuk AJAX (Search Real-time)
def search_user_json(request):
    query = request.GET.get('q', '')
    users = User.objects.filter(username__icontains=query)[:10] if query else []
    results = [{'username': user.username, 'id': user.id} for user in users]
    return JsonResponse({'data': results})

# View lainnya menggunakan Class Based Views
class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email']
    success_url = reverse_lazy('manage_users')

class UserDetailView(DetailView):
    model = User
    template_name = 'users/user_detail.html'

class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('manage_users')