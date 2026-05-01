from django.urls import path
from . import views

urlpatterns = [
    path('<str:module_id>/chapter/<str:chapter_id>/', views.showModule, name="showModule"),    
    path('<str:module_id>/quiz-prep/<str:quiz_id>/', views.quizPrep, name="quizPrep"),
    path('', views.manage_modules, name='manage_modules'),
    # Sesuaikan name='view_module' ini dengan yang akan dipanggil di HTML
    path('modules/<str:module_id>/chapter/<str:chapter_id>/', views.showModule, name='view_module'),
    path('<str:module_id>/editor/', views.module_editor, name='module_editor'),
    path('<str:module_id>/save/', views.save_module_content, name='save_module_content'),
]