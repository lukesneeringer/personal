from django.contrib.auth.decorators import login_required
from tools.shortcuts import template
from wedding.reservations.forms import RSVPForm
from wedding.reservations.models import *


@login_required
def index(request):
    """Return the RSVP landing page."""
    
    # pull up the invitation attached to this user
    invitation = Invitation.objects.get(user=request.user)
    
    # send down a template with reservation details
    return template(request, 'reservations/index.html', {
        'invitation': invitation,
    })
    
    
@login_required
def rsvp_form(request):
    """Provide or process a form for editing an RSVP."""
    
    # first, pull up the invitation and the reservation (if any)
    # for this user
    invitation = Invitation.objects.get(user=request.user)
    
    # okay, am I processing the form?
    forms = []
    if request.method == 'POST':
        # collect up all the forms
        for invitee in invitation.invitee_set.all():
            forms.append((invitee, RSVPForm(request.POST, instance=invitee.reservation)))
    
    # just collect up the blank forms
    for invitee in invitation.invitee_set.all():
        forms.append((invitee, RSVPForm(instance=invitee.reservation)))
        
    # send back the form
    return template(request, 'reservations/form.html', {
        'invitation': invitation,
        'forms': forms,
    })