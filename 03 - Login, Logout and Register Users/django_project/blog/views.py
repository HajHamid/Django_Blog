from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Count
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView, ListView

from .forms import CommentForm
from .models import Category, Comment, Like, Post, Read


class PostListView(ListView):
    model = Post
    template_name = "blog/home.html"
    context_object_name = "posts"
    ordering = "-date_posted"
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super(PostListView, self).get_context_data(**kwargs)
        context["in_slider_posts"] = Post.objects.filter(in_slider=True).order_by(
            "-date_posted"
        )
        context["categories"] = Category.objects.annotate(total_post=Count("post"))
        return context


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        user = get_object_or_404(User, id=request.user.id)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = user
            comment.save()
            messages.success(request, "نظر شما ثبت شد")
            return redirect("post-detail", pk)
    else:
        form = CommentForm()

    post = Post.objects.filter(id=pk).get()

    is_read = Read.objects.filter(post=post, user=request.user.id)
    is_like = Like.objects.filter(post=post, user=request.user.id)

    context = {"post": post, "is_read": is_read, "is_like": is_like, "form": form}
    return render(request, "blog/post_detail.html", context)


@login_required
def post_read(request, id):
    post = get_object_or_404(Post, id=id)
    user = get_object_or_404(User, id=request.user.id)
    if Read.objects.filter(post=post, user=user):
        Read.objects.filter(post=post, user=user).delete()
    else:
        r = Read(user=user, post=post)
        r.save()
    return HttpResponseRedirect(post.get_absolute_url())


@login_required
def post_like(request, id):
    post = get_object_or_404(Post, id=id)
    user = get_object_or_404(User, id=request.user.id)
    if Like.objects.filter(post=post, user=user):
        Like.objects.filter(post=post, user=user).delete()
    else:
        l = Like(user=user, post=post)
        l.save()
    return HttpResponseRedirect(post.get_absolute_url())


class CommentDeleteView(DeleteView):
    model = Comment

    def get_success_url(self):
        post = self.object.post
        return reverse_lazy("post-detail", kwargs={"pk": post.id})
