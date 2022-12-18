from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Post

# Serializer: 직렬화 하는 클래스
#             사용자 모델 인스턴스 -> Json/Dictionary 형태로 직렬화

# User의 username 가져오기
class UserSerializer(serializers.ModelSerializer):
    class Meta: # 특정 값 지정 가능
        model = User
        fields = ['username',]


# 모델로 만든 데이터와 1:1 매칭 => json 형태로 간단하게 변환
class postSerializer(serializers.ModelSerializer):
    author = UserSerializer(many=False, read_only=True)
    class Meta:
        model = Post
        fields = ['title', 'author', 'content', 'created_at']