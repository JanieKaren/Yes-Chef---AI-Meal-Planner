from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/user/', views.user_view, name='user'),
    path('ingredients/', views.ingredient_list, name='ingredient-list'),
    path('ingredients/<int:pk>/', views.ingredient_detail, name='ingredient-detail'),
] 