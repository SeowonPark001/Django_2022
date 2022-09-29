from django.db import models

# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=30)
    content = models.TextField()
    
    create_at = models.DateTimeField(auto_now_add=True) # 새로 작성 시 auto_now_add
    update_at = models.DateTimeField(auto_now=True)     # 수정(업데이트) 시 auto_now
    #author: 추후 작성 예정

    def __str__(self):
        # {self.pk} : 해당 포스트 pk 값 // {self.title} : 해당 포스트의 title 값값
       return f'[{self.pk}] {self.title}    {self.create_at}'   # ex) [1] Post_title_1

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'  # ex) localhost:8000/blog/1