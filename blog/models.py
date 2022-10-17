import os

from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True) # 미리보기 글
                    # char: 제한 가능 / text: 제한X
    content = models.TextField()

    # 9장(정적파일): 미디어 파일 저장
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)   # 이미지 파일 저장하는 ImageField
                                                        # %Y : 2022 // %y : 22
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)    # 파일 업로드를 위한 FileField

    created_at = models.DateTimeField(auto_now_add=True)    # 새로 작성 시 auto_now_add
    updated_at = models.DateTimeField(auto_now=True)         # 수정(업데이트) 시 auto_now
    #author: 추후 작성 예정

    def __str__(self):
        # {self.pk} : 해당 포스트 pk 값 // {self.title} : 해당 포스트의 title 값
       return f'[{self.pk}] {self.title}    {self.created_at}'   # ex) [1] Post_title_1

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'  # ex) localhost:8000/blog/1

    def get_file_name(self):
        return os.path.basename(self.file_upload.name) # 파일 이름만 반환 ex) abc.txt
        # self.file_upload.name : 파일 경로만 반환 ex) blog/files/abc.txt

    def get_file_ext(self): # 파일 확장자 얻기
        return self.get_file_name().split('.')[-1] # -1: 제일 마지막에 해당하는 단어 = 확장자