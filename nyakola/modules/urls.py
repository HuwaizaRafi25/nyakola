from django.urls import path
from . import views

urlpatterns = [
    path('<str:module_id>/chapter/<str:chapter_id>/', views.showModule, name="showModule"),    
    
]