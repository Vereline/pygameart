from django import forms
from .models import ArtUser
from django.contrib.auth.models import User


# test this form
class ArtUserForm(forms.ModelForm):

    """ Form for user to configure user's settings."""
    class Meta:
        model = ArtUser
        fields = ('birth_date', 'location', 'art_direction', 'description', 'user_avatar')


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )
        exclude = ('password', )
