"""Django_2022 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

# 9장(정적파일): url 처리
from django.conf import settings
from django.conf.urls.static import static

# DRF
# from rest_framework import routers
# from Django_2022.blog import views
#
# router = routers.DefaultRouter()
# router.register(r'tests', views.postViewSet)



# IP주소/~
urlpatterns = [
    path('admin/', admin.site.urls),        # IP주소/admin
    path('blog/', include('blog.urls')),    # IP주소/blog
    path('', include('single_pages.urls')), # IP주소/

    # 16장: allauth에서 제공하는 url => migrate만!
    path('accounts/', include('allauth.urls')), # IP주소/accounts/

    # DRF
    # path('drf/', include(router.urls)),       # IP주소/drf/
]

# 9장(정적파일): 미디어 파일을 위한 url 지정
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)