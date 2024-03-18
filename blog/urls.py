from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),
    path('', views.home, name='homepage'),
    path('create-blog/', views.blog_post, name="create-blog"),
    path('edit-blog/<str:pk>/', views.edit_blog, name="edit-blog"),
    path('delete-blog/<str:pk>/', views.delete_blog, name="delete-blog"),
    path('<slug:post>/', views.post_page, name='post_page'),
]