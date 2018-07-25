from django import forms
from .models import Contact


# test this form
class ContactForm(forms.ModelForm):

    """ Form for contact message."""
    class Meta:
        model = Contact
        fields = ('first_name', 'email', 'country', 'subject_text')
