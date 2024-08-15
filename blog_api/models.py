import os
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from datetime import timedelta

class DigitalMarketPost(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    download_link = models.URLField(max_length=200)
    image = models.ImageField(upload_to='digital_market_images/', blank=True, null=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    view_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    @classmethod
    def mark_old_posts_inactive(cls, minutes=4):
        threshold_date = timezone.now() - timedelta(minutes=minutes)
        old_posts = cls.objects.filter(created_at__lt=threshold_date)
        for post in old_posts:
            post.delete()
            print(f"{post} post(s) marked as inactive.")

class PriceForAdd(models.Model):
    TotalPrice = models.DecimalField(max_digits=10, decimal_places=2, blank=True, default=1000.00)
    ConnectCorrent = models.ForeignKey(User, on_delete=models.CASCADE)
    TranctionsAmount = models.DecimalField(max_digits=10, decimal_places=2, blank=True)
    DateTime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    post = models.ForeignKey(DigitalMarketPost, related_name='price_for_add', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.TotalPrice} - {self.ConnectCorrent.username}"


class BlogWriter(models.Model):
    userAccount = models.ForeignKey(User, verbose_name=("Linked User"), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cat = models.CharField(default="", max_length=20)
    subtitle = models.CharField(max_length=255)
    content = models.TextField()
    FavList = models.BooleanField(default=False)
    file = models.FileField(upload_to='uploads/')
    DateTime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    blog = models.ForeignKey(BlogWriter, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author} - {self.text[:20]}'
    
class UserProfile(models.Model):
    userAccount = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    phoneNo = models.CharField(max_length=15, null=True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    address = models.TextField(null=True, blank=True)

    

    
    
@receiver(models.signals.pre_delete, sender=PriceForAdd)
def delete_document_files(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, models.FileField):
            file_field = getattr(instance, field.name)
            if file_field:
                file_path = file_field.path
                if os.path.exists(file_path):
                    os.remove(file_path)
                    
                    
                    
