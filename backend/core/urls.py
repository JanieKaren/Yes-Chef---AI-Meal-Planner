from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views, auth

router = DefaultRouter()
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'accounts', views.AccountViewSet, basename='account')
router.register(r'ingredients', views.IngredientViewSet, basename='ingredient')

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', auth.register, name='register'),
    path('auth/login/', auth.login_view, name='login'),
    path('auth/logout/', auth.logout_view, name='logout'),
    path('auth/user/', auth.user_view, name='user'),
] 