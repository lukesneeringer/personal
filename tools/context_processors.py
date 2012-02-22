from django.core.urlresolvers import reverse

def data(request):
    """Add global template variables in..."""
    
    # global site nav
    nav = (
        {
            'area': 'about-luke',
            'label': 'About Luke',
        },
        {
            'area': 'about-meagan',
            'label': 'About Meagan',
        },
        {
            'area': 'directions',
            'label': 'Directions',
        },
        {
            'area': 'gifts',
            'label': 'Gifts',
        },
        {
            'area': 'photos',
            'label': 'Photos',
        },
        {
            'area': 'rsvp',
            'label': 'RSVP',
            'url': reverse('rsvp'),
        },
    )
    
    # done!
    return {
        'nav': nav,
    }