from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from cloudinary.models import CloudinaryField
from django.urls import reverse
from django.conf import settings
import os


def Default_Image():
    """Provides default image for articles"""
    return os.path.join(settings.MEDIA_URL, 'article_images/defaultimage.jpg')


class Post(models.Model):
    """Model for articles"""

    class NewManager(models.Manager):
        """Retrieves published posts using filter"""
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
    category = models.CharField(max_length=250, choices=categories,
                                default='gaming')
    publish = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='blog_posts')
    content = QuillField()
    status = models.CharField(max_length=10, choices=post_status,
                              default='publish')
    cover_picture = CloudinaryField('article-image', null=True)
    objects = models.Manager()
    new_manager = NewManager()

    def get_absolute_url(self):
        """Uses slug to define page url"""
        return reverse('blog:post_page', args=[self.slug])

    class Meta:
        """Reverses ordering, puts new articles first"""
        ordering = ('-publish',)

    def __str__(self):
        """For admin panel, returns legible string to make management easier"""
        return self.title


class Comments(models.Model):
    """Model for comments"""
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             related_name='comments', default=None)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = QuillField(max_length=250)
    created = models.DateTimeField()
    updated = models.DateTimeField()

    class Meta:
        """Reverses comment ordering, corrects issue with
        auto plurilisation of apps"""
        ordering = ('-created', '-updated')
        verbose_name_plural = "Comments"


class Poll(models.Model):
    """
    Model for polls.

    Stores the poll title, key and vote count.

    """

    categories = (
        ('gaming', 'Gaming'),
        ('film', 'Film'),
        ('books', 'Books')
    )

    title = models.CharField(max_length=250)
    category = models.CharField(max_length=250, choices=categories,
                                default='gaming')
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    thumbs_up_count = models.IntegerField(default=0)
    thumbs_down_count = models.IntegerField(default=0)


class Vote(models.Model):
    """
    Model for voting.

    Stores the users login, retrieves the poll and gives options to cast vote.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    thumbs_up = models.BooleanField(default=False)
    thumbs_down = models.BooleanField(default=False)
