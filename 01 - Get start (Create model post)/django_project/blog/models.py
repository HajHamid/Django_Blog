from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.OneToOneField(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to="post_pics/")
    date_posted = models.DateField(default=timezone.now)
    in_slider = models.BooleanField(default=False)

    def __str__(self):
        return self.title
