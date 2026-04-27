from django.urls import path
from . import views

urlpatterns = [
    path('<str:module_id>/chapter/<str:chapter_id>/', views.showModule, name="showModule"),    
    path('<str:module_id>/quiz-prep/<str:quiz_id>/', views.quizPrep, name="quizPrep"),
]