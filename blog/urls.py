from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('login/', views.login_page, name="login"),
    path('logout/', views.logout_page, name="logout"),
    path('register/', views.register_page, name="register"),
    path('', views.home, name='homepage'),
    path('create-blog/', views.blog_post, name="create-blog"),
    path('create-poll/', views.create_poll, name="create_poll"),
    path('edit-poll/<int:pk>', views.edit_poll, name="edit_poll"),
    path('delete-poll/<int:pk>', views.delete_poll, name="delete_poll"),
    path('delete_comment/<int:pk>', views.delete_comment, name="delete_comment"),
    path('edit-blog/<str:pk>/', views.edit_blog, name="edit-blog"),
    path('delete-blog/<str:pk>/', views.delete_blog, name="delete-blog"),
    path('<slug:post>/', views.post_page, name='post_page'),
    path('poll/<int:pk>/', views.poll_page, name='poll_page')
]