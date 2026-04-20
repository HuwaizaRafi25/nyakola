from django.shortcuts import render
from modules.views import get_all_modules

def list_modules_view(request):
    modules_data = get_all_modules()

    return render(request, 'manage_module.html', {'modules': modules_data})


# Create your views here.