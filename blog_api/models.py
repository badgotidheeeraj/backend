from django.db import models
import os
from django.dispatch import receiver
from django.contrib.auth.models import User


class BlogWriter(models.Model):
    userAccount = models.ForeignKey(User, verbose_name=("Linked User"), on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    cat=models.CharField(default="",max_length=20)
    subtitle = models.CharField(max_length=255)
    blog = models.TextField()
    FavList = models.BooleanField(default=False) # grations
    file = models.FileField(upload_to='uploads/')  
    DateTime = models.DateTimeField(auto_now_add=True)
    
class UserProfile(models.Model):
    userAccount = models.OneToOneField(User, on_delete=models.CASCADE)
    profilePic = models.ImageField(upload_to='profile_pics', blank=True, null=True)
    phoneNo = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    City = models.CharField(max_length=100, blank=True, null=True)
    Adress = models.TextField(blank=True, null=True)




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
class PriceForAdd(models.Model):
    TotalPrice = models.CharField(max_length=200,blank=True)
    ConnectCorrent = models.ForeignKey(User, on_delete=models.CASCADE)
    TranctionsAmount = models.CharField(max_length=200,blank=True)
    DateTime = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    def __str__(self):
        return self.TotalPrice
    
    
    
@receiver(models.signals.pre_delete, sender=PriceForAdd)
def delete_document_files(sender, instance, **kwargs):
    # Remove the file when the ReviewModule instance is deleted
    for field in instance._meta.fields:
        if isinstance(field, models.FileField):
            file_field = getattr(instance, field.name)
            if file_field:
                file_path = file_field.path
                if os.path.exists(file_path):
                    os.remove(file_path)