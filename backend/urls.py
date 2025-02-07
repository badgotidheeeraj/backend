from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path,include
from django.conf import settings

urlpatterns = [
    path('accounts/', include('registration.backends.simple.urls')),  # Default registration URLs
    path('admin/', admin.site.urls),
    # Your other URL patterns here
    path('', include('blog_api.urls')),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


admin.site.site_header = "Admin"
admin.site.site_title = "PenEcho Admin Portal"
admin.site.index_title = "Welcome to PenEcho Researcher Portal"


