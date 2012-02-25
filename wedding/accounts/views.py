from django.template.response import TemplateResponse
from wedding.accounts.forms import RegistrationForm


def register(request):
    """Allow the user to register for an account on the site."""
    
    # sanity check: is this a processing request?
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
    else:
        form = RegistrationForm()
        
    # return back the template
    return TemplateResponse(request, 'registration/register.html', {
        'form': form,
    })