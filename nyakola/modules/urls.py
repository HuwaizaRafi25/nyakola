from django.urls import path
from . import views

urlpatterns = [
    path('<>/chapter/<>', views.showModule, name="showModule"), 
    
]