from django import forms
from blog.models import Post, Comment
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['author', 'category', 'post_image', 'post_title', 'text']
        widgets = {
            # 'author': forms.TextInput(attrs = { 'class': 'textinputclass'}),
            # 'category': forms.Select(attrs={ 'class': 'textinputclass'}),

            # 'post_title':forms.TextInput(attrs={ 'class': 'textinputclass'}),
            # 'text': forms.Textarea(attrs={'class': 'postcontent'})
        }


class CommentForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs.update({'class': 'textinputclass'})
        self.fields['comment_text'].widget.attrs.update({'class': 'textinputclass'})

    class Meta:
        model = Comment

        fields = ('author', 'comment_text')
        # widget = {
        #     'author' : forms.TextInput(attrs={'class': 'textinputclass'}),
        #     'comment_text': forms.Textarea(attrs={'class': 'postcontent'})
        #
        #     # 'comment_text' : forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'})
        #   }


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
