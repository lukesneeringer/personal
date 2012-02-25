from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.context import get_standard_processors
from django.template.defaultfilters import date, yesno, timesince, timeuntil
from django.template.response import TemplateResponse
import jinja2


# set up the jinja template loaders
loaders = []
for path in settings.TEMPLATE_DIRS:
    loaders.append(jinja2.FileSystemLoader(path))
for app in settings.INSTALLED_APPS:
    loaders.append(jinja2.PackageLoader(app))
    
# create the jinja environment
jinja_env = jinja2.Environment(
    extensions=[
        'jinja2.ext.loopcontrols',
    ],
    line_statement_prefix='~ ',
    line_comment_prefix='# ',
    loader=jinja2.ChoiceLoader(loaders),
    trim_blocks=True,
)

# add django.core.urlresolvers.reverse as a global "url()" function
# that I can use in lieu of the {% url %} tag in django
jinja_env.globals['url'] = reverse

# add some of the filters from the Django core system that I like...
jinja_env.filters['format_date'] = date
jinja_env.filters['timesince'] = timesince
jinja_env.filters['timeuntil'] = timeuntil
jinja_env.filters['yesno'] = yesno


def template(request, filename, context={}, mimetype=None):
    """Return back an HttpResponse using the requested template.
    Do any feedmagnet-specific stuff that I want done foor every page before rendering"""
                    
    # I still want to keep the use of my Django context processors
    # even though this is a Jinja template; therefore, process them manually
    for context_processor in get_standard_processors():
        new_stuff = context_processor(request)
        if new_stuff:
            context.update(dict(new_stuff))
            
    # retrieve the appropriate template
    jinja_template = jinja_env.get_template(filename)
    response_text = jinja_template.render(context)
    return HttpResponse(response_text, mimetype=mimetype)