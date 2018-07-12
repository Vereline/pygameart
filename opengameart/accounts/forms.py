from django import forms
from .models import ArtUser
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.models import User


# test this form
class ArtUserForm(forms.ModelForm):

    """ Form for user to configure user's settings."""
    class Meta:
        model = ArtUser
        fields = ('birth_date', 'location', 'art_direction', 'description', 'user_avatar')
    # art = 'ART'
    # music = 'MUS'
    # video = 'VID'
    # text = 'TXT'
    # ART_DIRECTION = (
    #     (art, 'Art'),
    #     (music, 'Music'),
    #     (video, 'Video'),
    #     (text, 'Text'),
    # )

    # birth_date = forms.DateField(widget=forms.SelectDateWidget)
    # location = forms.CharField(max_length=255, label='location')
    # art_direction = forms.CharField(max_length=255, widget=forms.Select, label='art direction')
    # description = forms.CharField(widget=forms.Textarea, label='description')
    # user_avatar = forms.ImageField()
    #
    # user_id = forms.CharField(max_length=255, label='user id')  # than make user search by id and art search by id


class UserUpdateForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', )