from django.contrib import admin
from .models import BlogWriter, UserProfile, DigitalMarketPost,PriceForAdd


@admin.register(BlogWriter)
class BlogRegister(admin.ModelAdmin):
    list_display = ['id', 'userAccount', 'title', 'subtitle', 'blog', 'file', 'DateTime']


@admin.register(UserProfile)
class BlogRegisterCreate(admin.ModelAdmin):
    list_display = ['userAccount', 'profilePic', 'phoneNo', 'state', 'City', 'Adress', ]
    
    
admin.site.register(DigitalMarketPost)
class PostMarketing(admin.ModelAdmin):
    list_display = ['title','description','price','download_link','image','author','created_at','updated_at','view_count', ]




admin.site.register(PriceForAdd)
class PriceTransection(admin.ModelAdmin):
    list_display = ['TotalPrice','ConnectCorrent','TranctionsAmount','DateTime','view_count',]
