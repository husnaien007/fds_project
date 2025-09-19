# login/urls.py
from django.urls import path
from main import views

urlpatterns = [
    path('', views.blog_page, name='blog_page'),
    path('api/posts/', views.get_posts, name='get_posts'),
    path('api/crud/', views.blog_crud, name='blog_crud'),
]
