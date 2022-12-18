from django.urls import path
from . import views

urlpatterns = [ # ip주소/blog/
    # CBV
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),  # IP주소/blog/1

    # 13장 Category
    path('category/<str:slug>/', views.category_page),  # IP주소/blog/category/slug

    # 14장 Tag
    path('tag/<str:slug>/', views.tag_page),    # IP주소/blog/tag/slug

    # 15장 Form
    path('create_post/', views.PostCreate.as_view()),   # IP주소/blog/create_post
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),  # IP주소/blog/update_post/1

    # 17장 Comment Form
    path('<int:pk>/new_comment/', views.new_comment),  # IP주소/blog/post의 pk/new_comment/
    path('update_comment/<int:pk>/', views.CommentUpdate.as_view()),  # IP주소/blog/update_comment/1 : comment의 pk


    # FBV
    # path('', views.index),           # views.py 의 index 함수 내 포함되어있는 path
    # path('<int:pk>/', views.single_post_page),   # single_post_page 함수 내 포함되어있는 path
    # <자료형:변수명>

]