from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogWriter, UserProfile,DigitalMarketPost,Comment,PriceForAdd


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class BlogWriterSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogWriter
        fields = ['id', 'userAccount', 'title', 'cat', 'subtitle', 'content', 'FavList', 'file', 'DateTime']

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='author.username', read_only=True)
    class Meta:
        model = Comment
        fields = ['id', 'blog', 'author', 'text', 'created_at']
        read_only_fields = ['author', 'created_at']
# class CommentSerializer(serializers.ModelSerializer):
#     author_name = serializers.CharField(source='author.username', read_only=True)
    
#     class Meta:
#         model = Comment
#         fields = ['id', 'content', 'created_at', 'author_name', 'blog']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    userAccount = UserSerializer(read_only=True)  # Correctly reference the user data

    class Meta:
        model = UserProfile
        fields = ['id', 'userAccount', 'profilePic', 'phoneNo', 'state', 'City', 'Adress']
    
class PosterSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), required=False)

    class Meta:
        model = DigitalMarketPost
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['author'] = request.user
        return super().create(validated_data)
    
    
    
    
    
    
class DigitalMarketPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = DigitalMarketPost
        fields = [
            'id', 'title', 'description', 'price', 
            'download_link', 'image', 'author', 
            'created_at', 'updated_at', 'view_count'
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at', 'view_count']


class PriceForAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceForAdd
        fields = [
            'id', 'TotalPrice', 'ConnectCorrent', 
            'TranctionsAmount', 'DateTime', 'description', 'post'
        ]
        read_only_fields = ['id', 'DateTime', 'TotalPrice', 'TranctionsAmount']
