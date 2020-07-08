from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from users.forms import MyAuthForm
from users import views as users_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("blog.urls")),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="users/login.html", authentication_form=MyAuthForm
        ),
        name="login",
    ),
    path(
        "logout/",
        auth_views.LogoutView.as_view(template_name="users/logout.html"),
        name="logout",
    ),
    path("auth/", include("social_django.urls", namespace="social")),
    path("register/", users_views.register, name="register"),
    path("profile/", users_views.profile, name="profile"),
    path(
        "password_change",
        auth_views.PasswordChangeView.as_view(
            template_name="registration/password_change.html"
        ),
        name="password_change",
    ),
    path(
        "password_change/done/",
        auth_views.PasswordChangeDoneView.as_view(
            template_name="registration/password_change_done.html"
        ),
        name="password_change_done",
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
