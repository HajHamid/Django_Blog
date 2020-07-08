from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile


class MyAuthForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ["username", "password"]

    def __init__(self, *args, **kwargs):
        super(MyAuthForm, self).__init__(*args, **kwargs)
        self.fields["username"].widget = forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Username"}
        )
        self.fields["username"].label = False
        self.fields["password"].widget = forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Password"}
        )
        self.fields["password"].label = False


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)

        for fieldname in ["username", "email", "password1", "password2"]:
            self.fields[fieldname].label = False
            self.fields[fieldname].help_text = None

        self.fields["username"].widget.attrs["placeholder"] = "Username"
        self.fields["email"].widget.attrs["placeholder"] = "Email"
        self.fields["password1"].widget.attrs["placeholder"] = "Password"
        self.fields["password2"].widget.attrs["placeholder"] = "Retype password"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("A user with that email already exists.")
        else:
            return email


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)

        for fieldname in ["first_name", "last_name", "username", "email"]:
            self.fields[fieldname].label = False
            self.fields[fieldname].help_text = None

        self.fields["first_name"].widget.attrs["placeholder"] = "Firstname"
        self.fields["last_name"].widget.attrs["placeholder"] = "Lastname"

    def clean_email(self):
        email = self.cleaned_data.get("email")
        username = self.cleaned_data["username"]
        users = User.objects.filter(email__iexact=email).exclude(
            username__iexact=username
        )
        # if User.objects.filter(email=email).exists():
        if users:
            raise forms.ValidationError("A user with that email already exists.")
        else:
            return email


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ["image"]

    def __init__(self, *args, **kwargs):
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        self.fields["image"].label = False
        # self.fields["image"].widget.attrs["class"] = "custom-file-input"
