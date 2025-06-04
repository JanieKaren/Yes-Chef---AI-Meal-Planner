from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Account, Ingredient
from .serializers import UserSerializer, AccountSerializer, IngredientSerializer
from django.contrib.auth import login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.paginator import Paginator
from rest_framework.pagination import PageNumberPagination

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

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if not all([username, email, password]):
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

    user = User.objects.create_user(username=username, email=email, password=password)
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
