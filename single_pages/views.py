from django.shortcuts import render

# from Django_2022.blog.models import Post # 오류
# from ..blog.models import Post # 오류
# import os, sys
# from blog.models import Post
# sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))

from blog.models import Post # Problems 오류 무시하기....

# Create your views here.


def landing(request):
    # return render(request, 'single_pages/landing.html')

    recent_post = Post.objects.order_by('-pk')[:3] # 최신 포스트 3개

    return render(request, 'single_pages/landing.html',
                  {'recent_posts' : recent_post, }
    )

def about_me(request):
    return render(request, 'single_pages/about_me.html')