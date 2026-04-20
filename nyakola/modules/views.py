from django.shortcuts import redirect, render
from django.core.paginator import Paginator
from db_connection import modules_collection
from .models import Module
from .forms import ModuleForm
# Create your views here.
def manage_modul(request):
    if request.method == 'POST':
        form = ModuleForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_module')
        
    query = request.GET.get('q','')

    modules = Module.objects.all().order_by('-id')

    if query:
        modules = modules.filter(title__icontains=query)
    
    paginator = Paginator(modules, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'manage_module.html', {'page_obj': page_obj, 'query': query})

def get_all_modules():
    return list(modules_collection.find())