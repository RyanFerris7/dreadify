from django.forms import ModelForm
from django import forms
from django_quill.forms import QuillFormField
from .models import Post, Comments, Article

class CreateBlog(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'image_url', 'image', 'content']

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

class QuillPostForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ('title', 'slug', 'category', 'excerpt', 'category', 'article_image', 'article_image_url', 'content' )
