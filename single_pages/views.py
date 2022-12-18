from django.shortcuts import render


# Create your views here.


# def landing(request):
#     recent_post = Post.objects.order_by('-pk')[:3] # 221129 landing page
#
#     return render(request, 'single_pages/landing.html',
#                   {'recent_posts' : recent_post, } # 221129 landing page
#     )

def about_me(request):
    return render(request, 'single_pages/about_me.html')