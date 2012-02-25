from django.template.response import TemplateResponse


def home(request):
    """Wedding home page."""
    return TemplateResponse(request, 'static/home.html')
    
    
def info(request, template_name):
    """Display a static page, given the provided template name."""
    return TemplateResponse(request, 'static/%s.html' % template_name, {
        'area': template_name
    })
    