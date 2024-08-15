from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views_api
from .views_api import (AzureADLoginView, DigitalMarketPostListCreate, PriceForAddListCreate,UserProfileView,Blogger,singIN,CommentListCreateView,)

urlpatterns = [
    path('', views_api.welcome),
    path('login', views_api.login),
    path('sign-up', singIN.as_view()),
    path('user-profile', UserProfileView.as_view(), name='userProfile'),
    path('Blogger', Blogger.as_view(), name='userProfile'),
     path('Blogger/<int:id>/', Blogger.as_view(), name='blog_detail'),
    # path('add-campaign',DigitalMarketPostList.as_view()),
    path('delete/<int:id>', views_api.makedelete,),
    path('comments/',CommentListCreateView.as_view()),
    path('auth/azure/login/', AzureADLoginView.as_view(), name='azure_ad_login'),
     path('api/digitalmarketpost/', DigitalMarketPostListCreate.as_view(), name='digitalmarketpost-list-create'),
    path('api/priceforadd/', PriceForAddListCreate.as_view(), name='priceforadd-list-create'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# http://127.0.0.1:8000/searchapi/?search=g&datarange=2024-05-27
