# forms.py
from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']


from django.contrib.auth.forms import AuthenticationForm

class CustomLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control'
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control'
        })


from django.contrib.auth.models import Group, Permission
from django import forms

class GroupForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related("content_type"),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Permissions"
    )

    class Meta:
        model = Group
        fields = ["name", "permissions"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields["permissions"].label_from_instance = (
            lambda perm: perm.name
        )

    

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'featured_image', 'category', 'tags', ] 
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'featured_image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }  