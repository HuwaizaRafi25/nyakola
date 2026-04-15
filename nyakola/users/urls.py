from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserSinglePageView.as_view(), name='manage_users'),
    path('search-json/', views.search_user_json, name='search_user_json'),
    path('detail/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
    path('delete/<int:pk>/', views.UserDeleteView.as_view(), name='user_delete'),
]