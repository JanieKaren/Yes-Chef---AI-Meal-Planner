# recipes_api/urls.py
from django.urls import path
from .views import generate_recipes

urlpatterns = [
    path("recipes/", generate_recipes, name="generate_recipes"),
]
