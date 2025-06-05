from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter
from .views import AccountViewSet, UserViewSet

router = DefaultRouter()
router.register(r'accounts', AccountViewSet)
router.register(r'users', UserViewSet)


urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', views.logout_view, name='logout'),
    path('auth/user/', views.user_view, name='user'),
    path('ingredients/', views.ingredient_list, name='ingredient-list'),
    path('ingredients/<int:pk>/', views.ingredient_detail, name='ingredient-detail'),
    path('save-recipe/', views.recipe, name='save-recipe'),
    path('recipes-detail/<int:pk>/', views.recipe_detail, name='recipe-detail'),
] 