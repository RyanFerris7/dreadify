from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Post
from .forms import CreateBlog

# Create your views here.

def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'Username invalid.')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('blog:homepage')
        
        else:
            messages.error(request, 'Username or Password does not exist.')
    
    context = {}
    return render (request, 'login_register.html', context)

def logout_page(request):
    logout(request)
    return redirect('blog:homepage')

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    all_posts = Post.new_manager.filter(category__icontains=q)
    categories = Post.categories

    return render(request, 'index.html', {'posts' : all_posts, 'categories' : categories})


def post_page(request, post):

    post = get_object_or_404(Post, slug=post, status='publish')
    return render(request, 'post.html', {'post' : post})

@login_required(login_url='blog:login')
def blog_post(request):
    form = CreateBlog()
    if request.method == 'POST':
        form = CreateBlog(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:homepage')

    return render(request, 'blog_post.html', {'form' : form})

@login_required(login_url='blog:login')
def edit_blog(request, pk):
    blog = Post.objects.get(id=pk)
    form = CreateBlog(instance=blog)

    if request.user != Post.author:
        messages.error(request, 'Only the author can edit this post.')

    if request.method == 'POST':
        form = CreateBlog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:homepage')

    return render(request, 'blog_post.html', {'form' : form})

@login_required(login_url='blog:login')
def delete_blog(request, pk):
    blog = Post.objects.get(id=pk)

    if request.user != Post.author:
        messages.error(request, 'Only the author can delete this post.')

    if request.method == 'POST':
        blog.delete()
        return redirect('blog:homepage')

    return render(request, 'delete.html', {'obj':blog})



