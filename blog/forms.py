# 17장 댓글폼 :
from .models import Comment
from django import forms

class CommentForm(forms.ModelForm):
    class Meta: # 클래스 안의 클래스
        model = Comment
        fields = ('content', )  # 폼에서는 댓글 내용만