from django.urls import path
from . import views

urlpatterns = [
    # Jadi nanti link-nya adalah: /classes/modules/
    path('', views.manage_classes, name='manage_classes'),
    path('add/', views.add_class, name='add_class'),
    path('edit/<int:class_id>/', views.edit_class, name='edit_class'),
    path('delete/<int:class_id>/', views.delete_class, name='delete_class'),
    # path('modules/', views.manage_modules_view, name='manage_module') 
]