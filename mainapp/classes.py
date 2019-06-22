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
        if os.name == 'nt':
            html_path_arr = self.component.html_path.split('/')[4:]
            cwd_arr = os.getcwd().split('\\')
            # print('PATH', html_path_arr)
            win_html_path = os.path.join(settings.BASE_DIR, *html_path_arr)
            print(win_html_path)
            # import pdb; pdb.set_trace()
            with open(win_html_path, encoding='utf-8') as f:
                    html_string = f.read()
            return html_string
        else:
            with open(self.component.html_path) as f:
                html_string = f.read()
            return html_string

    def render(self, options=None):
        if options:
            print(options)
        html = self.template.render(self.context)
        return mark_safe(html)