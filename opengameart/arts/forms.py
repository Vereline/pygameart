from django import forms


# test this form
class ArtForm(forms.Form):
    """ Form for user to upload image."""
    title = forms.CharField(max_length=255)
    description = forms.CharField(widget=forms.Textarea)
    file = forms.ImageField(null=True, blank=True)
