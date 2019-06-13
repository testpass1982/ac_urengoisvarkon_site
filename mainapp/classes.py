from django.template import Context, Template
from django.utils.safestring import mark_safe
from django.conf import settings
import os

class SiteComponent:
    """composition class, wich renders self template with self context"""
    def __init__(self, component, context=None):
        self.component = component
        self.context = Context(context)

        self.template = Template(self.get_template_string())

    def get_template_string(self):
        # print('CWD: ', os.getcwd())
        # print('BASE_DIR: ', settings.BASE_DIR)
        with open(self.component.html_path) as f:
            html_string = f.read()
        return html_string

    def render(self, options=None):
        if options:
            print(options)
        html = self.template.render(self.context)
        return mark_safe(html)