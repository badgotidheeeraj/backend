from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from .serializer import (
    LoginSerializer, UserSerializer, PosterSerializer, BlogWriterSerializer, UserProfileSerializer,CommentSerializer,DigitalMarketPostSerializer, PriceForAddSerializer
)
from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status,permissions
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlogWriter, UserProfile, DigitalMarketPost,Comment,PriceForAdd
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .email_send import emailsender
from django.http import JsonResponse
import requests
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DigitalMarketPost, PriceForAdd
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import DigitalMarketPost, PriceForAdd
# from .serializers import DigitalMarketPostSerializer
from django.contrib.auth.models import User
from django.db import transaction




# Endpoint to welcome users
@api_view(['GET'])
def welcome(request):
    return Response({"success": True, "message": "Welcome to the system"})

# Endpoint to handle login
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            return Response({'refresh': str(refresh), 'access': str(refresh.access_token)})
        return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Endpoint to handle sign-up
@api_view(['POST'])
def sign_up(request):
    data = {
        'username': (request.data['first_name'] + request.data['last_name']).replace(' ', '').lower(),
        'email': request.data['email'],
        'first_name': request.data['first_name'],
        'last_name': request.data['last_name'],
        'password': request.data['password'],
    }
    serializer = UserSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        emailsender(data)
        return Response({"success": True, "data": data, 'user': serializer.data, 'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint to display blogs
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def BlogShow(request):
    try:
        search_query = request.query_params.get("search", '')
        module_name = request.query_params.get("category", '')

        all_requests = BlogWriter.objects.all().order_by('-DateTime')
        if search_query:
            all_requests = all_requests.filter(
                Q(title__icontains=search_query) | Q(cat__icontains=search_query))
        if module_name:
            all_requests = all_requests.filter(cat__icontains=module_name)

        serialized_data = BlogWriterSerializer(all_requests, many=True)
        response_data = {
            'success': True,
            'message': 'Request fetched successfully',
            "data": serialized_data.data,
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  

@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def BlogShowID(request, id):
    try:
        blog_data = get_object_or_404(BlogWriter, pk=id)
        serialized_data = BlogWriterSerializer(blog_data)
        return Response({"success": True, "data": serialized_data.data}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'POST'])
@permission_classes([permissions.IsAuthenticatedOrReadOnly])
def comment_list_create_view(request):
    if request.method == 'GET':
        blog_id = request.query_params.get('blog_id')
        if blog_id:
            comments = Comment.objects.filter(blog_id=blog_id)
            
        else:
            comments = Comment.objects.all()
        print(blog_id)
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        blog_id = request.data.get('blog')
        blog = get_object_or_404(BlogWriter, pk=blog_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user, blog=blog)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Endpoint to create a new blog
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def BlogWrite(request):
    context = {
        'userAccount': request.user.id,
        'title': request.data.get('title'),
        'subtitle': request.data.get('subtitle'),
        'blog': request.data.get('blog'),
        'FavList': request.data.get('FavList', False),
        'file': request.FILES.get('file'),
        'DateTime': request.data.get('DateTime'),
    }
    serialized_data = BlogWriterSerializer(data=context)
    if serialized_data.is_valid():
        serialized_data.save()
        return Response({"success": True, 'message': 'Request created successfully'}, status=status.HTTP_201_CREATED)
    return Response({"success": False, "message": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)

# Endpoint to get user data
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_userData(request):
    try:
        user_profile = UserProfile.objects.get(userAccount=request.user)
    except UserProfile.DoesNotExist:
        return Response({"success": False, "message": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serialized_data = UserProfileSerializer(user_profile)
    return Response({"success": True, "data": serialized_data.data}, status=status.HTTP_200_OK)

# Endpoint to list digital market posts
@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def digital_market_post_list(request):
    current_date = datetime.now().date()
    digital_market_posts = DigitalMarketPost.objects.filter(created_at__date=current_date).order_by('-created_at')

    for post in digital_market_posts:
        post.view_count += 1
        post.save()

    serialized_data = PosterSerializer(digital_market_posts, many=True)
    return Response({"success": True, "data": serialized_data.data}, status=status.HTTP_200_OK)

@api_view(['put'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def makedelete(request, id):
    try:
        digital_market_post = DigitalMarketPost.objects.get(id=id)
        digital_market_post.isActivate = False
        digital_market_post.isDelete = timezone.now() + timedelta(minutes=1) 
        digital_market_post.save()
        return Response({"success": True}, status=status.HTTP_200_OK)
    except DigitalMarketPost.DoesNotExist:
        return Response({"error": "Post not found"}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# ?ddskdfks;lfsdlkfj'sldkf'lsdkf;slkdf;'l


class AzureADLoginView(APIView):
    def post(self, request):
        token = request.data.get('token')

        if not token:
            return Response({'error': 'Token is required'}, status=400)

        # Validate the token
        user_info = self.validate_token(token)
        if not user_info:
            return Response({'error': 'Invalid token'}, status=401)

        # Authenticate user based on token information
        user = self.authenticate_with_azure_ad(user_info)
        if not user:
            return Response({'error': 'Authentication failed'}, status=401)

        # Generate JWT tokens for the user
        tokens = self.get_tokens_for_user(user)
        return Response(tokens)

    def validate_token(self, token):
        # Validate the token with Azure AD
        try:
            response = requests.get(
                'https://graph.microsoft.com/v1.0/me',
                headers={'Authorization': f'Bearer {token}'}
            )
            response.raise_for_status()
            return response.json()
        except requests.HTTPError:
            return None

    def authenticate_with_azure_ad(self, user_info):
        # Extract user details from Azure AD token
        email = user_info.get('mail') or user_info.get('userPrincipalName')
        if not email:
            return None

        # Check if user exists in Django
        user_model = get_user_model()
        user, created = user_model.objects.get_or_create(email=email,defaults={
            'username': email,
            # You can add more fields here, like `first_name` or `last_name` if available
        })

        # Additional logic can be added here if needed (e.g., update user info)
        
        return user

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        print(refresh.access_token)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }




from decimal import Decimal

class DigitalMarketPostListCreate(APIView):
    def get(self, request):
        posts = DigitalMarketPost.objects.all()
        serializer = DigitalMarketPostSerializer(posts, many=True)
        return Response(serializer.data)

    def post(self, request):
        user = request.user
        
        # Retrieve or create the user's balance
        user_balance, created = PriceForAdd.objects.get_or_create(
            ConnectCorrent=user,
            defaults={'TotalPrice': 1000.00, 'TranctionsAmount': 0.00}
        )
        
        # Check if the user has sufficient balance
        if user_balance.TotalPrice >= 5.00:
            user_balance.TotalPrice -= Decimal(5.00) or 5.00
            user_balance.TranctionsAmount = 5.00
            user_balance.description = f'Deducted 5 rupees for post "{request.data.get("title")}"'
            user_balance.save()

            # Create the post
            serializer = DigitalMarketPostSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(author=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'error': 'Insufficient balance to create a Digital Market Post.'}, status=status.HTTP_400_BAD_REQUEST)



from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
class PriceForAddListCreate(APIView):
    permission_classes = [IsAuthenticated]  # Ensure authentication

    def get(self, request):
        # Get current user using request.user
        current_user = request.user

        # Filter prices based on current user (ConnectCorrent field)
        prices = PriceForAdd.objects.filter(ConnectCorrent=current_user)
        serializer = PriceForAddSerializer(prices, many=True)

        return Response({"success": True, "data": serializer.data})

    def post(self, request):
        # Get current user for ConnectCorrent field
        current_user = request.user

        # Update serializer data to include current user
        serializer = PriceForAddSerializer(data=request.data)
        serializer.data['ConnectCorrent'] = current_user

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
