from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views_api
from .views_api import AzureADLoginView, DigitalMarketPostListCreate, PriceForAddListCreate

urlpatterns = [
    path('', views_api.welcome),
    path('login', views_api.login),
    path('bloger-creater', views_api.BlogWrite),
    path('sign-up', views_api.sign_up),
    path('show-blogger', views_api.BlogShow),
    path('show-userProfile', views_api.get_userData),
    path('add-campaign', views_api.digital_market_post_list),
    # path('add-createPost',views_api.createAddPost),
    path('delete/<int:id>', views_api.makedelete,),
    path('blogs/<int:id>/', views_api.BlogShowID),
    path('comments/', views_api.comment_list_create_view),
    path('auth/azure/login/', AzureADLoginView.as_view(), name='azure_ad_login'),
     path('api/digitalmarketpost/', DigitalMarketPostListCreate.as_view(), name='digitalmarketpost-list-create'),
    path('api/priceforadd/', PriceForAddListCreate.as_view(), name='priceforadd-list-create'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# http://127.0.0.1:8000/searchapi/?search=g&datarange=2024-05-27
