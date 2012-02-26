from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from wedding.accounts.forms import RegistrationForm
from wedding.reservations.models import Invitation


def register(request):
    """Allow the user to register for an account on the site."""
    
    # sanity check: is this a processing request?
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        
        # if the form is valid, create the user, log them in,
        # and send them on their way
        if form.is_valid():
            user = form.save()
            
            # associate the correct invitation with the user
            invitation = Invitation.objects.get(token=form.cleaned_data['token'])
            invitation.user = user
            invitation.save()
            
            # automatically log the user in
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'])
            login(request, user)
            
            # they probably want to go to the rsvp section...
            return HttpResponseRedirect(reverse('rsvp'))
    else:
        form = RegistrationForm()
        
    # return back the template
    return TemplateResponse(request, 'registration/register.html', {
        'form': form,
    })