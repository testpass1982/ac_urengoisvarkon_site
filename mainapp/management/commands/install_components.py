from django.core.management.base import BaseCommand
from mainapp.models import Component
from django.core.files import File
from django.conf import settings
import json
import os
import shutil

COMPONENT_FOLDER_NAME = 'component__'
COMPONENTS_FOLDER = os.path.join(settings.BASE_DIR, 'mainapp', 'templates', 'mainapp', 'components')
SCSS_FOLDER = os.path.join(settings.BASE_DIR, 'assets', 'scss', 'components')
JS_FOLDER = os.path.join(settings.BASE_DIR, 'static', 'js', 'components')
IMAGES_FOLDER = os.path.join(settings.BASE_DIR, 'static', 'images', 'components')

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.json_file = ''
        self.html_file = ''
        self.scss_file = ''
        self.js_file = ''
        #self.parameters
    def handle(self, *args, **options):
        for folder in os.listdir(COMPONENTS_FOLDER):
            if folder.startswith(COMPONENT_FOLDER_NAME):
                print('IT IS HERE', folder)
                if 'installed.lock' in os.listdir(os.path.join(COMPONENTS_FOLDER, folder)):
                    continue
                else:
                    for afile in os.listdir(os.path.join(COMPONENTS_FOLDER, folder)):
                        if afile.endswith('html'):
                            self.html_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                        if afile.endswith('scss'):
                            self.scss_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                        if afile.endswith('.js'):
                            self.js_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                        if afile.endswith('json'):
                            self.json_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                            with open(self.json_file, 'r') as json_file:
                                self.parameters = json.load(json_file)
                        if afile == 'images':
                            images_folder = os.path.join(COMPONENT_FOLDER_NAME, folder, afile)
                            for f in os.listdir(images_folder):
                                self.move_file_to_folder(f, IMAGES_FOLDER)

                    print(self.json_file)
                    print(self.html_file)
                    print(self.scss_file)
                    print(self.js_file)
                    print(self.parameters)
                    self.move_file_to_folder(self.scss_file, SCSS_FOLDER)
                    self.move_file_to_folder(self.js_file, JS_FOLDER)
                    self.component_title = folder.split('__')
                    self.update_parameters()
                    # import pdb; pdb.set_trace()
                    self.create_component_object(self.parameters)
                    self.create_lock_file({'file': 'installed.lock'})

    def move_file_to_folder(self, afile, folder):
        try:
            print('moving a file {}'.format(afile))
            shutil.move(afile, folder)
            print('-------->file moved to {}'.format(folder))
        except:
            print('NO FILE in {}'.format(folder))

    def update_parameters(self):
        scss_file_path = os.path.join(SCSS_FOLDER, os.path.basename(self.scss_file))
        js_file_path = os.path.join(JS_FOLDER, os.path.basename(self.js_file))
        self.parameters.update({'html_path': self.html_file})
        self.parameters.update({'scss_path': scss_file_path})
        self.parameters.update({'js_path': js_file_path})
        self.parameters.update({'title': self.component_title})
        print('***parameters updated: ', self.parameters)

    def create_component_object(self, *options):
        component = Component.objects.create(options)
        print('*** COMPONENT CREATED: ', component.title, component.pk)

    def add_link_to_base_html(self, afile):
        pass

    def create_lock_file(self, *options):
        with open(options['file'], 'w') as f:
            data = "component installed {}".format(self.component_title)
            f.write(data)
