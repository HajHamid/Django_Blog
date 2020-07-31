from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="blog-home"),
    path("post/<int:pk>/", views.post_detail, name="post-detail"),
    path("post/<int:id>/read/", views.post_read, name="post-read"),
    path("post/<int:id>/like/", views.post_like, name="post-like"),
    path(
        "comment/<int:pk>/delete/",
        views.CommentDeleteView.as_view(),
        name="comment-delete",
    ),
    path("search/", views.search_post, name="search-post"),
    path(
        "search/users/<str:username>/",
        views.UserPostListView.as_view(),
        name="user-post",
    ),
    path(
        "search/tags/<str:tag_name>/", views.TagPostListView.as_view(), name="tag-post"
    ),
]

