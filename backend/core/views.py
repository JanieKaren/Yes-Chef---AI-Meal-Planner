from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Account, Ingredient, Recipe
from .serializers import UserSerializer, AccountSerializer, IngredientSerializer, RecipeSerializer
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from datetime import timedelta

# Create your views here.

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)
    
    def get_object(self):
        return self.request.user

class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise permissions.PermissionDenied("You can only update your own account")
        return obj

    @action(detail=True, methods=['post'])
    def update_dietary_preferences(self, request, pk=None):
        account = self.get_object()
        if account.user != request.user:
            raise permissions.PermissionDenied("You can only update your own dietary preferences")
        account.dietary_preferences = request.data.get('dietary_preferences', [])
        account.save()
        return Response(self.get_serializer(account).data)

    @action(detail=True, methods=['post'])
    def update_fridge_inventory(self, request, pk=None):
        account = self.get_object()
        if account.user != request.user:
            raise permissions.PermissionDenied("You can only update your own fridge inventory")
        account.fridge_inventory = request.data.get('fridge_inventory', [])
        account.save()
        return Response(self.get_serializer(account).data)
    
    @action(detail=True, methods=['post'])
    def update_allergies(self, request, pk=None):
        account = self.get_object()
        if account.user != request.user:
            raise permissions.PermissionDenied("You can only update your own allergies")
        account.allergies = request.data.get('allergies', [])
        account.save()
        return Response(self.get_serializer(account).data)



@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    firstname = request.data.get('firstname') 
    lastname = request.data.get('lastname') 
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([firstname,lastname, username, email, password]):
        return Response(
            {'error': 'Please provide all required fields'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {'error': 'Username already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(first_name=firstname, last_name=lastname,username=username, email=email, password=password)
    login(request, user)

    return Response({
        'user': UserSerializer(user).data,
        'account': AccountSerializer(user.account).data
    })

@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')

    if not all([username, password]):
        return Response(
            {'error': 'Please provide both username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    if not user.check_password(password):
        return Response(
            {'error': 'Invalid credentials'},
            status=status.HTTP_401_UNAUTHORIZED
        )

    login(request, user)

    return Response({
        'user': UserSerializer(user).data,
        'account': AccountSerializer(user.account).data
    })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    logout(request)
    return Response({'message': 'Successfully logged out'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_view(request):
    return Response({
        'user': UserSerializer(request.user).data,
        'account': AccountSerializer(request.user.account).data
    })

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def ingredient_list(request):
    if request.method == 'GET':
        ingredients = Ingredient.objects.filter(user=request.user)
        
        # Apply search filter
        search_query = request.GET.get('search')
        if search_query:
            ingredients = ingredients.filter(name__icontains=search_query)
        
        # Apply category filter
        category = request.GET.get('category')
        if category:
            ingredients = ingredients.filter(category=category)
        
        # Apply condition filter
        condition = request.GET.get('condition')
        print(f"Received condition parameter: {condition}")  # Debug log
        if condition:
            today = timezone.now().date()
            print(f"Today's date: {today}")  # Debug log
            
            if condition == 'expired':
                ingredients = ingredients.filter(expiration_date__lt=today)
                print(f"Filtering expired items: {ingredients.count()}")  # Debug log
            elif condition == 'expiring_soon':
                ingredients = ingredients.filter(
                    expiration_date__gte=today,
                    expiration_date__lte=today + timedelta(days=3)
                )
                print(f"Filtering expiring soon items: {ingredients.count()}")  # Debug log
            elif condition == 'expiring_week':
                ingredients = ingredients.filter(
                    expiration_date__gt=today + timedelta(days=3),
                    expiration_date__lte=today + timedelta(days=7)
                )
                print(f"Filtering expiring this week items: {ingredients.count()}")  # Debug log
            elif condition == 'good':
                ingredients = ingredients.filter(expiration_date__gt=today + timedelta(days=7))
                print(f"Filtering good items: {ingredients.count()}")  # Debug log
        
        # Order by expiration date
        ingredients = ingredients.order_by('expiration_date')
        
        paginator = Paginator(ingredients, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        serializer = IngredientSerializer(page_obj, many=True)
        
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'results': serializer.data,
        })

    elif request.method == 'POST':
        serializer = IngredientSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def ingredient_detail(request, pk):
    try:
        ingredient = Ingredient.objects.get(pk=pk, user=request.user)
    except Ingredient.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = IngredientSerializer(ingredient)
        return Response(serializer.data)

    elif request.method in ['PUT', 'PATCH']:
        serializer = IngredientSerializer(ingredient, data=request.data, partial=request.method == 'PATCH')
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        ingredient.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    

@api_view(['GET','POST'])
@permission_classes([IsAuthenticated])
def recipe(request):
    if request.method == 'GET':
        # Filter recipes by current user
        recipes = Recipe.objects.filter(user=request.user)
        # Apply search filter
        search_query = request.GET.get('search')
        if search_query:
            recipes = recipes.filter(title__icontains=search_query)
        
        # Apply favorite filter
        favorite = request.GET.get('favorite')
        if favorite:
            recipes = recipes.filter(favorite=True)
        
        paginator = Paginator(recipes, 9)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        serializer = RecipeSerializer(page_obj, many=True)
        return Response({
            'count': paginator.count,
            'num_pages': paginator.num_pages,
            'current_page': page_obj.number,
            'next_page': page_obj.next_page_number() if page_obj.has_next() else None,
            'previous_page': page_obj.previous_page_number() if page_obj.has_previous() else None,
            'results': serializer.data,
        })

    elif request.method == 'POST':
        serializer = RecipeSerializer(data=request.data)
        if serializer.is_valid():
            # Save with user attached
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', 'DELETE'])
@permission_classes([IsAuthenticated])
def recipe_detail(request, pk):
    try:
        recipe = Recipe.objects.get(pk=pk, user=request.user)
    except Recipe.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        # Partial update: for favorite toggle or other fields
        data = request.data
        serializer = RecipeSerializer(recipe, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        recipe.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
