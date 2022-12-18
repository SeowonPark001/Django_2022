from django.urls import path
from . import views

urlpatterns = [ # IP 주소/
    # landing
    path('', views.about_me),            # IP주소
    path('about_me/', views.about_me),  # IP주소/about_me/
]