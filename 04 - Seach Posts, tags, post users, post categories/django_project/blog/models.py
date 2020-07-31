from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.safestring import mark_safe
from markdown_deux import markdown
from taggit.managers import TaggableManager

from .utils import get_read_time


class Category(models.Model):
    category = [("info", "تالیفی"), ("success", "ترجمه ای"),
                ("warning", "کاربران")]
    name = models.CharField(max_length=20, choices=category, default="info")

    def __str__(self):
        return self.name


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    brief = models.CharField(max_length=300)
    content = models.TextField()
    image = models.ImageField(upload_to="post_pics/")
    date_posted = models.DateTimeField(default=timezone.now)
    in_slider = models.BooleanField(default=False)
    read_time = models.TimeField(null=True, blank=True)
    tags = TaggableManager()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post-detail", kwargs={"pk": self.id})

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


class Read(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, blank=True, related_name="likes"
    )


class Comment(models.Model):
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(User, unique=False, on_delete=models.CASCADE)
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    is_approved = models.BooleanField(default=False)

    class Meta:
        ordering = ["-date_created"]

    def __str__(self):
        return self.text
