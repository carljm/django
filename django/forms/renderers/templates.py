import os

from django import forms
from django.template import TemplateDoesNotExist
from django.template.backends.django import DjangoTemplates
from django.template.loader import get_template
from django.utils.functional import cached_property

try:
    import jinja2
except ImportError:
    jinja2 = None

ROOT = os.path.dirname(forms.__file__)


class TemplateRenderer(object):
    def get_template(self, template_name):
        try:
            return get_template(template_name)
        except TemplateDoesNotExist:
            # TODO: Add RemovedInDjango20Warning indicating this fallback will be removed.
            return self.default_engine.get_template(template_name)

    def render(self, template_name, context, request=None):
        template = self.get_template(template_name)
        return template.render(context, request=request).strip()

    @cached_property
    def default_engine(self):
        if jinja2:
            from django.template.backends.jinja2 import Jinja2
            return Jinja2({
                'APP_DIRS': False,
                'DIRS': [os.path.join(ROOT, 'jinja2')],
                'NAME': 'djangoforms',
                'OPTIONS': {},
            })
        return DjangoTemplates({
            'APP_DIRS': False,
            'DIRS': [os.path.join(ROOT, 'templates')],
            'NAME': 'djangoforms',
            'OPTIONS': {},
        })
