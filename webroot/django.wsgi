#!/usr/bin/env python
import os
import sys

# --------------------------------
# -- general mod_wsgi bootstrap --
# --------------------------------
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()