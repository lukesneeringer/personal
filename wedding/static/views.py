from tools.shortcuts import template

def home(request):
    """Wedding home page."""
    return template(request, 'home.html')
    
    
def info(request, template_name):
    """Display a static page, given the provided template name."""
    return template(request, '%s.html' % template_name, {
        'area': template_name
    })
    