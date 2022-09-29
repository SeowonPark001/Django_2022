from django.urls import path
from . import views

urlpatterns = [
    # CBV
    path('', views.PostList.as_view()),
    path('<int:pk>/', views.PostDetail.as_view()),

    # FBV
    #path('', views.index),           # views.py 의 index 함수 내 포함되어있는 path
    #path('<int:pk>/', views.single_post_page),   # single_post_page 함수 내 포함되어있는 path
    # <자료형:변수명>

]