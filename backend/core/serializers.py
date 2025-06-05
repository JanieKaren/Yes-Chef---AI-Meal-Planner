from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Account, Ingredient, Recipe

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')
        read_only_fields = ['id'] 

class AccountSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Account
        fields = ('id', 'user', 'dietary_preferences', 'saved_recipes', 'allergies')

class IngredientSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Ingredient
        fields = ('id', 'user', 'name', 'icon_name', 'category', 'expiration_date', 'quantity', 'unit')
        read_only_fields = ('user',)


class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'updated_at']