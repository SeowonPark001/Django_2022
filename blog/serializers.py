from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username',]

class postSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'content', 'created_at']