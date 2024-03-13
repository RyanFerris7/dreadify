from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Post(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='publish')

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
    image = models.ImageField(upload_to='article_images', null=True)
    objects = models.Manager()
    new_manager = NewManager()

    def get_absolute_url(self):
        return reverse('blog:post_page', args=[self.slug])
    
    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title
