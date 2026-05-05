from django.urls import path
from . import views

urlpatterns =[
    # Jadi nanti link-nya adalah: /classes/modules/
    path('', views.manage_classes, name='manage_class'),
    path('add/', views.add_class, name='add_class'),
    path('edit/<str:class_id>/', views.edit_class, name='edit_class'),
    path('delete-class/<str:class_id>/', views.delete_class, name='delete_class'),
    path('get-class-details/<str:class_id>/', views.get_class_details, name='get_class_details'), 
    path('modules/', views.manage_modules, name='manage_modules')
]

