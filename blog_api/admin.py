from django.contrib import admin
from django.db.models.signals import post_save
from django.contrib.admin.models import LogEntry
from django.utils.timezone import now
from .models import (
    BlogWriter, UserProfile, DigitalMarketPost, 
    PriceForAdd, Comment, Transaction, UserActivityLog
)


@admin.register(BlogWriter)
class BlogRegister(admin.ModelAdmin):
    list_display = ['id', 'userAccount', 'title', 'subtitle', 'content', 'file', 'DateTime']


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['userAccount', 'profilePic', 'phoneNo', 'state', 'city', 'address']
    

@admin.register(DigitalMarketPost)
class PostMarketing(admin.ModelAdmin):
    list_display = [
        'id', 'title', 'description', 'price', 'download_link', 'image', 
        'author', 'created_at', 'updated_at', 'view_count'
    ]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['id', 'blog', 'author', 'text', 'created_at']


@admin.register(PriceForAdd)
class PriceTransection(admin.ModelAdmin):
    list_display = ['TotalPrice', 'ConnectCorrent', 'TranctionsAmount', 'DateTime']  
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['user', 'transaction_type', 'amount', 'recipient', 'timestamp', 'description']



# ✅ Function to Log Admin Actions
@admin.register(UserActivityLog)
class UserActivityLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'action', 'url', 'timestamp', 'ip_address', 'user_agent')
    # list_filter = (('timestamp', DateRangeFilter),)
    search_fields = ('user__username', 'action', 'url', 'ip_address')
    # list_filter = ('timestamp',)


def log_admin_action(sender, instance, **kwargs):
    if instance.user:  # Ensure user exists
        UserActivityLog.objects.create(
            user=instance.user,
            action=f"Admin {instance.get_action_flag_display()} - {instance.object_repr}",
            timestamp=now(),
            ip_address="Admin Panel",
            user_agent="Admin Panel",
        )


# ✅ Connect LogEntry signals
post_save.connect(log_admin_action, sender=LogEntry)
