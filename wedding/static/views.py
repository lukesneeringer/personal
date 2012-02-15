from tools.shortcuts import template

def home(request):
    """Wedding home page."""
    
    return template(request, 'home.html')
    
    
def info(request):
    pass