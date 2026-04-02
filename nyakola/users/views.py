from django.shortcuts import redirect
from django.views.generic import ListView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DeleteView
from django.urls import reverse_lazy

class UserSinglePageView(ListView):
    model = User
    template_name = 'users/manage_users.html'
    context_object_name = 'semua_user'

    # Menambahkan form ke dalam context agar bisa muncul di HTML
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = UserCreationForm() 
        return context

    # Menangani logika Create (POST) di halaman yang sama
    def post(self, request, *args, **kwargs):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('manage_users')
        return self.get(request, *args, **kwargs)
    
class UserDeleteView(DeleteView):
    model = User
    success_url = reverse_lazy('manage_users')