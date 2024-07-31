from django.shortcuts import render
from rest_framework.response import Response
from .serializer import LoginSerializer, UserSerializer, PosterSerializer, BlogerSerializer, UserProfileSerializer  # ,userProfile # ,# ModulesSerializer, FetchSchemaSerializer, CreateRequestSerializer, FetchRequestsSerializer, FetchRequestSchemaSerializer, ResourceSerializer, UpdateRequestSchemaSerializer, ProfileSerializer,ChangePasswordSerializer
from django.contrib.auth import authenticate
from datetime import datetime
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .models import BlogWriter, UserProfile, DigitalMarketPost
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from django.utils import timezone
from .email_send import emailsender  # Make sure to import your utility function


 
@api_view(['GET'])
def welcome(request):
    return Response({"success": True, "message": "Welcome to the system"})
# ?login


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
        else:
            return Response({'success': False, 'message': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    return Response({"success": False, "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    


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



@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def BlogShow(request):
    try:
        # paginator = PageNumberPagination()
        # paginator.page_size = 3
        search_query = request.query_params.get("search", '')
        module_name = request.query_params.get("category", '')

        all_requests = BlogWriter.objects.all().order_by('-DateTime')
        # print(BlogWriter.objects.filter(
        #     userAccount__user=request.user))#.order_by('-DateTime'))

        if search_query:
            all_requests = all_requests.filter(
                Q(title__icontains=search_query) | Q(cat__icontains=search_query))
        if module_name:
            all_requests = all_requests.filter(
                cat__icontains=module_name)
        if hasattr(all_requests, '__iter__'):
            # paginated_queryset = paginator.paginate_queryset(
            #     all_requests, request)
            serialized_data = BlogerSerializer(
                all_requests, many=True)
            # current_page = paginator.page.number
            # total_pages = paginator.page.paginator.num_pages
            # next_page = current_page + 1 if paginator.page.has_next() else None
            # prev_page = current_page - 1 if paginator.page.has_previous() else None
        response_data = {
            'success': True,
            'message': 'Request fetched successfully',
            "data": serialized_data.data,
            # "pagination": {
            #     "total_records": paginator.page.paginator.count,
            #     "current_page": current_page,
            #     "total_pages": total_pages,
            #     "next_page": next_page,
            #     "prev_page": prev_page,
            # }
        }
        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({'success': False, 'errors': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# 
from django.shortcuts import  get_object_or_404


@api_view(['GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def BlogShowID(request, id):
    try:
        blog_data = BlogWriter.objects.get(pk=id)
        # blog_writer = get_object_or_404(BlogWriter, userAccount__first_name='dheeraj')
        # context = {
        #     'blog_writer': blog_writer,
        # }
        # print(context)
        serialized_data = BlogerSerializer(blog_data)
        return Response({"success": True, "data": serialized_data.data}, status=status.HTTP_200_OK)

    except BlogWriter.DoesNotExist:
        return Response({"success": False, "error": "BlogWriter does not exist"}, status=status.HTTP_404_NOT_FOUND)

    except Exception as e:
        return Response({"success": False, "error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def BlogWrite(request):
    context = {
        'userAccount': request.user.id,
        'title': request.data.get('title'),
        'subtitle': request.data.get('subtitle'),
        'blog': request.data.get('blog'),
        'FavList': request.data.get('FavList', False),  # Default to False if not provided
        'file': request.FILES.get('file'),  # Get the file from the request
        'DateTime': request.data.get('DateTime'),  # Handle DateTime if needed
    }
    print(context)
    serialized_data = BlogerSerializer(data=context)
    if serialized_data.is_valid():
        serialized_data.save()
        return Response({"success": True, 'message': 'Request created successfully'}, status=status.HTTP_201_CREATED)
    else:
        return Response({"success": False, "message": serialized_data.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['get'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_userData(request):
    try:
        user_profile = UserProfile.objects.get(userAccount=request.user)
    except UserProfile.DoesNotExist:
        return Response({"success": False, "message": "User profile not found."}, status=status.HTTP_404_NOT_FOUND)

    serialized_data = UserProfileSerializer(user_profile)
    return Response({"success": True, "data": serialized_data.data}, status=status.HTTP_200_OK)


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def createAddPost(request):
    serializer = PosterSerializer(data=request.data, context={'request': request})
    if serializer.is_valid():
        serializer.save(author=request.user)
        return Response({"success": True, "data": serializer.data}, status=status.HTTP_201_CREATED)
    
    return Response({"success": False, "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)