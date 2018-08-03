from django import forms
from arts.models import ArtComment


class ArtForm(forms.Form):
    """ Form for user to upload image."""
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    file = forms.ImageField()


class ArtCommentForm(forms.ModelForm):

    class Meta:
        model = ArtComment
        fields = ('author', 'text',)
