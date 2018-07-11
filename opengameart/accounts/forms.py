from django import forms


# test this form
class ArtUserForm(forms.Form):
    """ Form for user to configure user's settings."""

    art = 'ART'
    music = 'MUS'
    video = 'VID'
    text = 'TXT'
    ART_DIRECTION = (
        (art, 'Art'),
        (music, 'Music'),
        (video, 'Video'),
        (text, 'Text'),
    )

    username = forms.CharField(max_length=255)
    password = forms.PasswordInput()
    email = forms.EmailField()

    birth_date = forms.DateField()
    location = forms.CharField(max_length=255)
    art_direction = forms.CharField(max_length=255, choices=ART_DIRECTION)
    description = forms.CharField(widget=forms.Textarea)
    user_avatar = forms.ImageField()

    user_id = forms.CharField(max_length=255)
