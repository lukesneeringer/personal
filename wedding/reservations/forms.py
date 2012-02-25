# encoding: utf8
from django import forms
from wedding.reservations.models import RSVP


class RSVPForm(forms.ModelForm):
    """A form for creating or modifying an RSVP."""
    
    required_css_class = 'required'
    error_css_class = 'error'
    
    class Meta:
        exclude = ('invitee', 'medium')
        model = RSVP
        widgets = {
            'accepts': forms.RadioSelect,
        }
        
    def __init__(self, *args, **kwargs):
        super(RSVPForm, self).__init__(*args, **kwargs)
        self.fields['food'].widget = forms.RadioSelect(choices=RSVP._meta.get_field_by_name('food')[0].choices)
        
    def clean(self):
        """If an invitee is unable to attend, then clear out their food order."""
        
        if not bool(self.cleaned_data['accepts']):
            self.cleaned_data['food'] = None
        return self.cleaned_data
        