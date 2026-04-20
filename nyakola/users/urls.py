from django.urls import path
from . import views

urlpatterns = [# READ: Menampilkan list user
    path('', views.user_list, name='user_list'), 
    
    # CREATE: Halaman/fungsi tambah user
    path('add/', views.add_user, name='add_user'), 
    
    # UPDATE: Edit user berdasarkan ID
    path('edit/<str:id>/', views.update_user, name='edit_user'), 
    
    # DELETE: Hapus user berdasarkan ID
    path('delete/<str:id>/', views.delete_user, name='delete_user')
]