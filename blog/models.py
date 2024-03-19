from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.conf import settings
import os


def Default_Image():
    return os.path.join(settings.MEDIA_URL, 'article_images/defaultimage.jpg')

class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status='publish')

    post_status = (
        ('draft', 'Draft'),
        ('publish', 'Publish')
    )

    categories = (
        ('gaming', 'Gaming'),
        ('film', 'Film'),
        ('books', 'Books')
    )

    title = models.CharField(max_length=250)
    excerpt = models.TextField(max_length=250, null=True)
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    category = models.CharField(max_length=250, choices=categories, default='gaming')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    content = models.TextField()
    status = models.CharField(max_length=10, choices=post_status, default='draft')
    image_url = models.URLField(blank=True)
    image = models.ImageField(upload_to='article_images', null=True, default=Default_Image)
    objects = models.Manager()
    new_manager = NewManager()

    def get_absolute_url(self):
        return reverse('blog:post_page', args=[self.slug])
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Comments(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField(max_length=250)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        ordering = ('-created', '-updated')
        verbose_name_plural = "Comments"

    def __str__(self):
        return self.content[:25]



class Poll(models.Model):
    title = models.CharField(max_length=250)
    thumbs_up_count = models.IntegerField(default=0)
    thumbs_down_count = models.IntegerField(default=0)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    thumbs_up = models.BooleanField(default=True)
    thumbs_down = models.BooleanField(default=False)


