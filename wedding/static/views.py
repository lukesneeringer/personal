from django.template.response import TemplateResponse


def home(request):
    """Wedding home page."""
    return TemplateResponse(request, 'static/home.html')
    
    
def info(request, template_name):
    """Display a static page, given the provided template name."""
    return TemplateResponse(request, 'static/%s.html' % template_name, {
        'area': template_name
    })
    
def photo(request, orientation, id):
    """Display a specific photo."""
    
    # what is the filename for the photo that has been clicked on?
    filename = '%s%d.jpg' % (orientation, int(id))
    
    # return back the template
    return TemplateResponse(request, 'static/photo.html', {
        'area': 'photos',
        'filename': filename,
        'orientation': orientation,
    })