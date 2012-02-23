from django.contrib.auth.decorators import login_required
from tools.shortcuts import template
from wedding.reservations.models import *


@login_required
def index(request):
    """Return the RSVP landing page."""
    
    # pull up the invitation attached to this user
    invitation = Invitation.objects.get(user=request.user)
    
    # send down a template with reservation details
    return template(request, 'index.html', {
        'invitation': invitation,
    })