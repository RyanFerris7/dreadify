from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home, name='homepage'),
    path('create-blog/', views.blog_post, name="create-blog"),
    path('<slug:post>/', views.post_page, name='post_page'),

]