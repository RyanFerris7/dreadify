from django.forms import ModelForm
from .models import Post

class CreateBlog(ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'excerpt', 'content', 'status']