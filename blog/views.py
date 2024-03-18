from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Post
from .forms import CreateBlog

# Create your views here.

def login_page(request):
    page = 'login'
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
    
    context = {'page':page}
    return render (request, 'login_register.html', context)

def logout_page(request):
    logout(request)
    return redirect('blog:homepage')

def register_page(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            #Creates object in memory, could use this to 
            #check manage entered details if needed
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('blog:homepage')
        
        else:
            messages.error(request, 'An error has occured, please check your details.')

    return render(request, 'login_register.html', { 'form': form })

def home(request):

    q = request.GET.get('q') if request.GET.get('q') != None else ''

    all_posts = Post.new_manager.filter(category__icontains=q)
    categories = Post.categories

    return render(request, 'index.html', {'posts' : all_posts, 'categories' : categories})


def post_page(request, post):
    post_object = get_object_or_404(Post, slug=post, status='publish')
    comments = post_object.comments.all()  # Accessing comments related to the post
    context = {'post': post_object, 'comments': comments}
    return render(request, 'post.html', context)

@login_required(login_url='blog:login')
def blog_post(request):
    form = CreateBlog()
    if request.method == 'POST':
        form = CreateBlog(request.POST)
        if form.is_valid():
            #Creates object in memory, adds user as author then saves it
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
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



