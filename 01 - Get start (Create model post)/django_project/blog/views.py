from django.shortcuts import render
from django.views.generic import ListView
from .models import Post


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = "-date_posted"

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context["in_slider_posts"] = Post.objects.filter(in_slider=True).order_by(
            "-date_posted"
        )
        return context
