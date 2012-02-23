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
            'area': 'travel',
            'label': 'Travel Information',
        },
        {
            'area': 'rsvp',
            'label': 'RSVP',
            'url': reverse('rsvp'),
        },
        {
            'area': 'photos',
            'label': 'Photos',
        },
        {
            'area': 'gifts',
            'label': 'Gifts',
        },
    )
    
    # done!
    return {
        'nav': nav,
    }