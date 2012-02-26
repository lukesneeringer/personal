from django import forms
from django.contrib.auth.forms import UserCreationForm
from wedding.reservations.models import Invitation


class RegistrationForm(UserCreationForm):
    token = forms.CharField(
        help_text='Enter the token provided to you on your invitation response card. Case insensitive.',
        max_length=11,
    )
    
    def clean_token(self):
        """Ensure validity of the user's registration token."""
        
        # transform this code to all lowercase, and remove the hyphen
        # if it's present
        token = self.cleaned_data['token'].replace('-', '').lower()
        
        # if the token is not in the database, then error out
        if Invitation.objects.filter(token=token).count() == 0:
            raise forms.ValidationError, 'That token was not found.'
            
        # another possibility is that the token has already been used--test for this;
        # don't allow multiple accounts on the same invitation
        if Invitation.objects.filter(token=token).exclude(user=None).count() > 0:
            raise forms.ValidationError, 'There is already a user account registered for this token.'
            
        # okay, we're good to go...
        return token