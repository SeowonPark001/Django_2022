from django.shortcuts import render
from .models import Post
from django.views.generic import ListView

# ListView 로 포스트 목록 페이지 만들기
# class PostList(ListView):
#     model = Post
#     ordering = '-pk'

def index(request):
    # 모델명.objects.all() => 모든 post 가져오기
    # pk 역순(-)으로 정렬(나열)
    posts = Post.objects.all().order_by('-pk')

    return render(
        request,
        'blog/index.html',  # 사용할 템플릿
        {
            'posts': posts  # 템플릿에 넘겨줄 값 => 딕셔너리 형태 { 'key': value }
        }
    )


def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )