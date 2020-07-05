from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.utils import timezone
from django.utils.safestring import mark_safe

from markdown_deux import markdown

from .utils import get_read_time


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to="post_pics/")
    date_posted = models.DateField(default=timezone.now)
    in_slider = models.BooleanField(default=False)
    read_time = models.TimeField(null=True, blank=True)

    def __str__(self):
        return self.title

    def get_markdown(self):
        content = self.content
        markdown_text = markdown(content)
        return mark_safe(markdown_text)


def pre_save_post_reciver(sender, instance, *args, **kwargs):
    if instance.content:
        html_string = instance.get_markdown()
        read_time_var = get_read_time(html_string)
        instance.read_time = read_time_var


pre_save.connect(pre_save_post_reciver, sender=Post)
