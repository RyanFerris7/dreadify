from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Poll(models.Model):
    title = models.CharField(max_length=250)
    thumbs_up_count = models.IntegerField(default=0)
    thumbs_down_count = models.IntegerField(default=0)

class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    thumbs_up = models.BooleanField(default=True)
    thumbs_down = models.BooleanField(default=False)

