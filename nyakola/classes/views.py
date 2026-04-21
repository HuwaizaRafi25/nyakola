from django.shortcuts import render
from modules.views import manage_modul 

def manage_classes(request):
    return render(request, 'manage_class.html')
    
def add_class(request):
    return render(request, 'add_class.html')

def edit_class(request, class_id):
    return render(request, 'edit_class.html', {'class_id': class_id})

def delete_class(request, class_id):
    return render(request, 'delete_class.html', {'class_id': class_id})