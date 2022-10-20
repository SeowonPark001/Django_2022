import os
from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) # 미리보기 글
                    # char: 제한 가능 / text: 제한X
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)  # 새로 작성 시 auto_now_add
    updated_at = models.DateTimeField(auto_now=True)  # 수정(업데이트) 시 auto_now

    # 9장(정적파일): 미디어 파일 저장
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   # 이미지 파일 저장하는 ImageField
                                                        # %Y : 2022 // %y : 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)    # 파일 업로드를 위한 FileField

    # 13장: 작성자                   # on_delete=models.CASCADE : user가 삭제되면 post도 같이 없어진다
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL) # <- 괄호() X
                                    # null=True 반드시 필요 // SET_NULL: user가 삭제되면 null(none)로 바꿈 >> post 그대로 유지

    def __str__(self):
        # {self.pk} : 해당 포스트 pk 값 // {self.title} : 해당 포스트의 title 값
        # {self.pk}] {self.title}    {self.created_at}'   # ex) [1] Post_title_1  2022.01.01 00:00:00
       return f'[{self.pk}] {self.title}::{self.author} _ {self.created_at}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'  # ex) localhost:8000/blog/1

    def get_file_name(self):
        return os.path.basename(self.file_upload.name) # 파일 이름만 반환 ex) abc.txt
        # self.file_upload.name : 파일 경로만 반환 ex) blog/files/abc.txt

    def get_file_ext(self): # 파일 확장자 얻기
        return self.get_file_name().split('.')[-1] # -1: 제일 마지막에 해당하는 단어 = 확장자