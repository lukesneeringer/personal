from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from wedding.reservations.models import *


@login_required
def index(request):
    """Return the RSVP landing page."""
    
    # send down a template with reservation details
    return TemplateResponse(request, 'reservations/index.html', {
        'invitation': request.user.invitation,
    })
    
@login_required
def rsvp_form(request):
    """Provide or process a form for editing an RSVP."""
    
    # first, pull up the invitation and the reservation (if any)
    # for this user
    invitation = request.user.invitation
    
    # okay, am I processing the form?
    forms = []
    if request.method == 'POST':
        # collect up all the forms
        for invitee in invitation.invitee_set.all():
            forms.append((invitee, invitee.get_rsvp_form(request.POST)))
            
        # process each form and save to the database
        if reduce(lambda x, y: x & y, [form.is_valid() for invitee, form in forms]):
            for invitee, form in forms:
                rsvp = form.save(commit=False)
                rsvp.medium = 'online'
                rsvp.save()
                
        # we're successful; provide a message and self-redirect
        return HttpResponseRedirect(reverse('rsvp-thanks'))
    else:
        # the user is asking to rsvp -- give him a form to fill out
        for invitee in invitation.invitee_set.all():
            forms.append((invitee, invitee.get_rsvp_form()))
        
    # send back the form
    return TemplateResponse(request, 'reservations/form.html', {
        'invitation': invitation,
        'forms': forms,
    })
    

@login_required
def rsvp_thanks(request):
    """Landing page for a successful RSVP."""
    
    # retrieve the invitation
    invitation = request.user.invitation
    
    # return the template
    return TemplateResponse(request, 'reservations/thanks.html', {
        'invitation': invitation,
    })