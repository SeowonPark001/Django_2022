from django.contrib import admin

# Register your models here.
# 관리자 페이지에 모델 등록

from .models import Post, Category, Tag, Comment

# Register Posts
admin.site.register(Post)

# 13장 다대일: 카테고리 모델 등록
class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Category, CategoryAdmin)


# 14장 다대다: 태그 모델 등록
class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name', )}

admin.site.register(Tag, TagAdmin)


# 17장: 댓글 모델 등록
admin.site.register(Comment)