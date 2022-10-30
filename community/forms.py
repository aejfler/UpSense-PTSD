from django import forms
from taggit.forms import TagWidget

from community.models import Comment, Post


class CreatePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'tags')
        exclude = ('author', )
        widgets = {
            'tags': TagWidget(),
        }


class SearchForm(forms.Form):
    search = forms.CharField(max_length=50)


class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'category', 'content', 'tags')
        exclude = ('author', )
        widgets = {
            'tags': TagWidget()
        }


class DeletePostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = '__all__'


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': '4',
            }),
        }
        labels = {
            'content': "",
        }


class EditCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', )
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': '4',
            }),
        }
        labels = {
            'content': "",
        }


class DeleteCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = '__all__'
