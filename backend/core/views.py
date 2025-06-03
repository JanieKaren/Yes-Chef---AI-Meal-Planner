from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Account, Ingredient
from .serializers import UserSerializer, AccountSerializer, IngredientSerializer

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    @action(detail=True, methods=['post'])
    def update_dietary_preferences(self, request, pk=None):
        account = self.get_object()
        account.dietary_preferences = request.data.get('dietary_preferences', [])
        account.save()
        return Response(self.get_serializer(account).data)

    @action(detail=True, methods=['post'])
    def update_fridge_inventory(self, request, pk=None):
        account = self.get_object()
        account.fridge_inventory = request.data.get('fridge_inventory', [])
        account.save()
        return Response(self.get_serializer(account).data)

class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save()

    def get_queryset(self):
        return Ingredient.objects.all()
