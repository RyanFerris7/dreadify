from django.shortcuts import render, get_object_or_404
from .models import Post

# Create your views here.

def home(request):

    all_posts = Post.new_manager.all()


    return render(request, 'index.html', {'posts' : all_posts})


def post_page(request, post):

    post = get_object_or_404(Post, slug=post, status='publish')

    return render(request, 'post.html', {'post' : post})


def blog_post(request):

    return render(request, 'blog_post.html')