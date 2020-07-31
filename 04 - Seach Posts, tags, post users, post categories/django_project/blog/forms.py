from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields["text"].label = False
        self.fields["text"].widget.attrs[
            "placeholder"
        ] = "نظری بنویسید و Enter را فشار دهید"

        self.fields["text"].widget.attrs["rows"] = "1"
