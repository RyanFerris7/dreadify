from django.forms import ModelForm
from .models import Post, Comments

class CreateBlog(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'image_url', 'image', 'content', 'status']

class CommentForm(ModelForm):
    class Meta:
        model = Comments
        fields = ['content']

