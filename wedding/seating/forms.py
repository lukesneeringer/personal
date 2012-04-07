from django import forms
from wedding.seating.models import Seat


class SeatForm(forms.ModelForm):
    """Form to add validation for seats."""
    
    def clean_person(self):
        # sanity check: make sure this person is actually
        # attending the wedding
        person = self.cleaned_data['person']
        if not person.accepts:
            raise forms.ValidationError, 'This person is not attending the wedding, and therefore cannot have a seat.'
            
        return self.cleaned_data