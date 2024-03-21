from django.forms import ModelForm
from django import forms
from django_quill.forms import QuillFormField
from .models import Post, Comments, Poll

class CreateBlog(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'category', 'excerpt', 'cover_picture', 'content']

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

class CreatePoll(ModelForm):
    class Meta:
        model = Poll
        fields = ['title', 'category']