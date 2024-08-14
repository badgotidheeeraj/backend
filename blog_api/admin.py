from django.contrib import admin
from .models import BlogWriter, UserProfile, DigitalMarketPost,PriceForAdd,Comment


@admin.register(BlogWriter)
class BlogRegister(admin.ModelAdmin):
    list_display = ['id', 'userAccount', 'title', 'subtitle', 'content', 'file', 'DateTime']


@admin.register(UserProfile)
class BlogRegisterCreate(admin.ModelAdmin):
    list_display = ['userAccount', 'profilePic', 'phoneNo', 'state', 'City', 'Adress', ]
    
    
@admin.register(DigitalMarketPost)
class PostMarketing(admin.ModelAdmin):
    list_display = ['id','title','description','price','download_link','image','author','created_at','updated_at','view_count']
@admin.register(Comment)
class PostMarketingComment(admin.ModelAdmin):
    list_display = ['id', 'blog', 'author', 'text', 'created_at']

admin.site.register(PriceForAdd)
class PriceTransection(admin.ModelAdmin):
    list_display = ['TotalPrice','ConnectCorrent','TranctionsAmount','DateTime','view_count',]

