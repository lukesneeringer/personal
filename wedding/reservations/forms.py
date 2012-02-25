from django import forms
from wedding.reservations.models import RSVP


class RSVPForm(forms.ModelForm):
    """A form for creating or modifying an RSVP."""
    
    class Meta:
        exclude = ('invitee', 'medium')
        model = RSVP