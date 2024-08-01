from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BlogWriter, UserProfile,DigitalMarketPost


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class BlogerSerializer(serializers.ModelSerializer):

    class Meta:
        model = BlogWriter
        fields = ['id', 'userAccount', 'title', 'subtitle', 'cat', 'blog', 'FavList', 'file', 'DateTime']

    def create(self, validated_data):
        return BlogWriter.objects.create(**validated_data)

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
        fields = ['title', 'description', 'price', 'download_link', 'image', 'author', 'created_at', 'updated_at']

    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, "user"):
            validated_data['author'] = request.user
        return super().create(validated_data)