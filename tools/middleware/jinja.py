from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.template.context import get_standard_processors
from django.template.defaultfilters import date, yesno, timesince, timeuntil
from django.template.response import TemplateResponse
from django import template
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


class JinjaTemplateResponse(TemplateResponse):
    def resolve_context(self, context):
        if context:
            context = dict(context)
        else:
            context = {}
        
        # I still want to keep the use of my Django context processors
        # even though this is a Jinja template; therefore, process them manually
        for context_processor in get_standard_processors():
            new_stuff = context_processor(self._request)
            if new_stuff:
                context.update(dict(new_stuff))
    
        # return a flat dict; jinja doesn't have context objects
        return context
    
    def resolve_template(self, template):
        """Takes a template and tries to return back the appropriate
        Jinja template object.
        If an explicit Django template object is passed, do nothing."""
        
        if isinstance(template, basestring):
            return jinja_env.get_template(template)
        elif isinstance(template, (list, tuple)):
            return jinja_env.select_template(template)
        else:
            return template