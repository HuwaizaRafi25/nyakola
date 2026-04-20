from django.urls import path
from . import views

urlpatterns = [
    # URL ini akan jadi nyakola.com/classes/modules/
    path('modules/', views.manage_modul, name='manage_module.html'),
]