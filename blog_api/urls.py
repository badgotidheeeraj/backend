from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views_api

urlpatterns = [
    path('',views_api.welcome),
    path('login', views_api.login),    
    path('bloger-creater',views_api.BlogWrite),
    path('bloger-creater-id/<int:id>',views_api.BlogShowID),
    path('sign-up',views_api.sign_up),
    path('show-blogger',views_api.BlogShow),
    path('show-userProfile',views_api.get_userData),
    path('add-campaign',views_api.digital_market_post_list),
    path('add-createPost',views_api.createAddPost),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# http://127.0.0.1:8000/searchapi/?search=g&datarange=2024-05-27
