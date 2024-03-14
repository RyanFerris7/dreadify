from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from .forms import CreateBlog

# Create your views here.

def home(request):

    all_posts = Post.new_manager.all()


    return render(request, 'index.html', {'posts' : all_posts})


def post_page(request, post):

    post = get_object_or_404(Post, slug=post, status='publish')
    return render(request, 'post.html', {'post' : post})


def blog_post(request, pk):
    form = CreateBlog()
    if request.method == 'POST':
        form = CreateBlog(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:homepage')

    return render(request, 'blog_post.html', {'form' : form})

def edit_blog(request, pk):
    blog = Post.objects.get(id=pk)
    form = CreateBlog(instance=blog)

    if request.method == 'POST':
        form = CreateBlog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:homepage')

    return render(request, 'blog_post.html', {'form' : form})

def delete_blog(request, pk):
    blog = Post.objects.get(id=pk)
    if request.method == 'POST':
        blog.delete()
        return redirect('blog:homepage')

    return render(request, 'delete.html', {'obj':blog})