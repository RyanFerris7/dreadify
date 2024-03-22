from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.urls import reverse
from random import shuffle
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.utils.text import slugify
from .models import Post, Poll, Vote, Comments
from .forms import CreateBlog, CommentForm, CreatePoll

# Create your views here.#
def login_status_check(user):
    """
    View function for checking login status.

    Used to prevent access to certain pages if logged in.
    """
    return not user.is_authenticated

@user_passes_test(login_status_check, login_url='blog:homepage')
def login_page(request):
    """
    View function that manages user login.
    Renders the login form, and then attempts to validate credentials.

    Checks login status, redirects user if already logged in.

    If credentials match, the user is logged in.
    If credentials are invalid, an error message is displayed. 
    """
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
    """
    View function that manages user logout.

    Logs the user out, and then redirects to website homepage. 
    """
    logout(request)
    return redirect('blog:homepage')

def register_page(request):
    """
    View function that manages user registration.

    If registration is successful, user is logged in and redirected to homepage.
    If registration fails, an error message is displayed.
    """
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            login(request, user)
            return redirect('blog:homepage')

        else:
            messages.error(request, 'An error has occured, please check your details.')

    return render(request, 'login_register.html', { 'form': form })

def home(request):
    """
    View function for website homepage and querying.

    Renders homepage, polls and published articles. 
    Enables article and poll sorting by category.
    Enables article shuffling, for further reading.

    """
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    all_posts = Post.new_manager.filter(category__icontains=q)
    categories = Post.categories
    polls = Poll.objects.all()
    all_polls = Poll.objects.filter(category__icontains=q)
    shuffled_articles = list(all_posts)
    shuffle(shuffled_articles)
    user_authenticated = request.user.is_authenticated

    return render(request, 'index.html', {'posts' : all_posts, 'shuffled_articles': shuffled_articles, 'categories' : categories, 'polls':all_polls})

def about(request):
    """
    View function for about page.
    Details website and how to use.
    """
    return render(request, 'about.html')

def post_page(request, post):
    """
    View function for website article pages. 

    Uses slug of article to return specific article.

    Renders article with comments, and comment form.
    If comment form is valid, saves the comment to the article.
    """
    post_object = get_object_or_404(Post, slug=post, status='publish')
    comments = post_object.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            if request.user.is_authenticated:

                comment = form.save(commit=False)
                comment.post = post_object
                comment.author = request.user
                comment.created = timezone.now()
                comment.updated = timezone.now()
                comment.save()
                return redirect('blog:post_page', post=post)
            else:
                messages.error(request, 'You must be logged in to comment.')
    else: 
        form = CommentForm() 

    context = {'post': post_object, 'comments': comments, 'form': form}
    return render(request, 'post.html', context)

@login_required(login_url='blog:login')
def create_poll(request):
    """
    View function for creating polls.

    If the form is valid, the poll is saved and rendered.
    """
    form = CreatePoll(initial={'title':''})
    if request.method == 'POST':
        form = CreatePoll(request.POST)
        if form.is_valid():
            create_poll = form.save(commit=False)
            create_poll.author = request.user
            create_poll.save()
            return redirect('blog:homepage')

    return render(request, 'create_poll.html', {'form' : form})

@login_required(login_url='blog:login')
def edit_poll(request, pk):
    """
    View function for editing poll.

    The primary key of the poll is used to specify the poll being edited.

    A user must be logged in to access this function.

    Checks if the user attempting to edit the poll is the author. 
    If the user is not the author, an error message is displayed.
    If the user is the author, an article edit option is displayed.

    Retrieves current content from the article and allows changes to be made. 

    If the article edit form is valid, the article is updated and rendered.
    The user is then returned to the homepage.
    """
    poll = Poll.objects.get(id=pk)
    form = CreatePoll(instance=poll)

    if request.user != poll.author:
        messages.error(request, 'Only the author can edit this poll.')
        return redirect('blog:homepage')

    if request.method == 'POST':
        form = CreatePoll(request.POST, instance=poll)
        if form.is_valid():
            form.save()
            return redirect('blog:homepage')

    return render(request, 'create_poll.html', {'form' : form})

@login_required(login_url='blog:login')
def delete_poll(request, pk):
    """
    View function that manages deleting articles.
    The primary key of the article is used to specify the article being deleted.

    A user must be logged in to access this function. 

    Checks if the user is author of the article.
    If the user is not the author, an error message is displayed.
    If the user is the author, an article delete option is displayed.

    After deletion, the user is returned to the homepage. 

    """
    poll = Poll.objects.get(id=pk)

    if request.user != poll.author:
        messages.error(request, 'Only the author can delete this poll.')
        return redirect('blog:homepage')

    if request.method == 'POST':
        poll.delete()
        messages.success(request, 'The post has been deleted.')
        return redirect('blog:homepage')

    return render(request, 'delete.html', {'obj':poll})

@login_required(login_url='blog:login')
def delete_comment(request, pk):
    """
    View function that manages deleting comments.
    The primary key is used to specify the comment.

    A user must be logged in to access this function. 

    Checks if the user is author of the comment.
    If the user is not the author, an error message is displayed.
    If the user is the author, a comment delete option is displayed.

    After deletion, the user is returned to the homepage. 

    """
    comment = Comments.objects.get(id=pk)

    if request.user != comment.author:
        messages.error(request, 'Only the author can delete this comment.')
        return redirect('blog:homepage')

    if request.method == 'POST':
        post_slug = comment.post.slug
        comment.delete()
        messages.success(request, 'The comment has been deleted.')
        return redirect(reverse('blog:post_page', args=[post_slug]))

    return render(request, 'delete.html', {'obj':comment})

@login_required(login_url='blog:login')
def blog_post(request):
    """
    View function for creating article pages.

    Creates article object in memory, adds logged in user to it.
    If the form is valid, the article is saved and rendered.
    """
    form = CreateBlog(initial={'title':'', 'excerpt':''})
    if request.method == 'POST':
        form = CreateBlog(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.slug = slugify(blog_post.title)
            blog_post.save()
            return redirect('blog:homepage')
        else:
            messages.error(request, 'An error has occurred.')

    return render(request, 'blog_post.html', {'form' : form})


@login_required(login_url='blog:login')
def edit_blog(request, pk):
    """
    View function for editing blog.

    The primary key of the article is used to specify the article being edited.

    A user must be logged in to access this function.

    Checks if the user attempting to edit the article is the author. 
    If the user is not the author, an error message is displayed.
    If the user is the author, an article edit option is displayed.

    Retrieves current content from the article and allows changes to be made. 

    If the article edit form is valid, the article is updated and rendered.
    The user is then returned to the homepage.
    """
    blog = Post.objects.get(id=pk)
    form = CreateBlog(instance=blog)

    if request.user != blog.author:
        messages.error(request, 'Only the author can edit this post.')
        return redirect('blog:homepage')

    if request.method == 'POST':
        form = CreateBlog(request.POST, instance=blog)
        if form.is_valid():
            form.save()
            return redirect('blog:homepage')

    return render(request, 'blog_post.html', {'form' : form})

@login_required(login_url='blog:login')
def delete_blog(request, pk):
    """
    View function that manages deleting articles.
    The primary key of the article is used to specify the article being deleted.

    A user must be logged in to access this function. 

    Checks if the user is author of the article.
    If the user is not the author, an error message is displayed.
    If the user is the author, an article delete option is displayed.

    * Note - Still needs a message display to warn the user that this cannot be undone *

    After deletion, the user is returned to the homepage. 

    """
    blog = Post.objects.get(id=pk)

    if request.user != blog.author:
        messages.error(request, 'Only the author can delete this post.')
        return redirect('blog:homepage')

    if request.method == 'POST':
        blog.delete()
        messages.success(request, 'The post has been deleted.')
        return redirect('blog:homepage')

    return render(request, 'delete.html', {'obj':blog})

@login_required(login_url='blog:login')
def poll_page(request, pk):
    """
    View function for managing polls, and users voting on polls.

    Users must be logged in to access this function.

    Uses primary key to identify poll.

    Checks if a user has already voted, and displays an error message.

    If the user votes 'thumbs_up', adds to poll count.
    If the user votes 'thumbs_down', adds to poll count.

    Updates and renders the poll. 
    """
    poll = get_object_or_404(Poll, id=pk)
    user = request.user
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    all_posts = Post.new_manager.filter(category__icontains=q)
    categories = Post.categories
    polls = Poll.objects.all()

    thumbs_up = request.GET.get('thumbs_up')
    thumbs_down = request.GET.get('thumbs_down')
    already_voted = Vote.objects.filter(user=user, poll=poll).exists()

    if already_voted:
        messages.error(request, 'You have already cast a vote in this poll.')
 
    else:
        if thumbs_up:
            poll.thumbs_up_count += 1
            poll.save()
            Vote.objects.create(user=user, poll=poll, thumbs_up=True)

        elif thumbs_down:
            poll.thumbs_down_count += 1
            poll.save()
            Vote.objects.create(user=user, poll=poll, thumbs_down=True)

        else:
            messages.error(request, 'An error has occurred, please try again.')

    return render(request, 'index.html', {'posts' : all_posts, 'categories' : categories, 'polls':polls})

def dreadify_404(request, exception):
    """
    View function for 404 page.

    Python function to return a custom 404 page for better user experience.
    """
    return render(request, '404.html', status=404)