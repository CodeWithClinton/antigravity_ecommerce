from rest_framework.decorators import api_view, permission_classes
from django_api_readme.decorators import api_doc
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserSerializer, RegisterInputSerializer, LoginInputSerializer

User = get_user_model()

@api_doc(RegisterInputSerializer, UserSerializer, summary="Register User", description="Create a new user account.")
@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')

    if not email or not username or not password:
        return Response(
            {'error': 'Please provide email, username, and password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    if User.objects.filter(email=email).exists():
        return Response(
            {'error': 'Email already exists'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(email=email, username=username, password=password)
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_doc(LoginInputSerializer, summary="User Login", description="Authenticate a user and return JWT tokens along with user data.")
@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    email = request.data.get('email')
    password = request.data.get('password')

    if not email or not password:
        return Response(
            {'error': 'Please provide email and password'}, 
            status=status.HTTP_400_BAD_REQUEST
        )

    user = authenticate(email=email, password=password)
    
    if user is None:
        return Response(
            {'error': 'Invalid credentials'}, 
            status=status.HTTP_401_UNAUTHORIZED
        )
        
    if not user.is_active:
        return Response(
            {'error': 'Account is inactive'}, 
            status=status.HTTP_403_FORBIDDEN
        )

    refresh = RefreshToken.for_user(user)
    serializer = UserSerializer(user)

    return Response({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': serializer.data
    }, status=status.HTTP_200_OK)
