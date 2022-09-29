from django.urls import path
from . import views

urlpatterns = [
    #path('', views.PostList.as_view()), # ListView로 포스트 목록 페이지 만들기 >> (모델명)_list.html을 템플릿으로 인지
    path('', views.index),           # views.py 의 index 함수 내 포함되어있는 path

    path('<int:pk>/', views.single_post_page),   # single_post_page 함수 내 포함되어있는 path
    # <자료형:변수명>

]