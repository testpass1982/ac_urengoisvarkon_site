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
JS_FOLDER = os.path.join(settings.BASE_DIR, 'static', 'js')
IMAGES_FOLDER = os.path.join(settings.BASE_DIR, 'static', 'img')
SCSS_RELATIVE_FOLDER = 'scss/components/'
JS_RELATIVE_FOLDER = 'js/'
TEMPLATE_RELATIVE_FOLDER = 'mainapp/components/'
IMAGES_RELATIVE_FOLDER = 'img/'

class Command(BaseCommand):
    def __init__(self):
        super().__init__()
        self.template_folder_name = ''
        self.json_file = ''
        self.html_file = ''
        self.scss_file = ''
        self.js_file = ''
        self.component_title = ''
        #self.parameters
    def handle(self, *args, **options):
        for folder in os.listdir(COMPONENTS_FOLDER):
            self.component_title = folder.split('__')[1]
            if folder.startswith(COMPONENT_FOLDER_NAME):
                print('FOUND COMPONENT FOLDER', folder)
                self.template_folder_name = folder
                if 'installed.lock' in os.listdir(os.path.join(COMPONENTS_FOLDER, folder)):
                    print('it is already installed')
                    continue
                else:
                    for afile in os.listdir(os.path.join(COMPONENTS_FOLDER, folder)):
                        if afile.endswith('html'):
                            self.html_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                        if afile.endswith('scss'):
                            self.scss_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                        if afile.endswith('js'):
                            self.js_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                        if afile.endswith('json'):
                            self.json_file = os.path.join(COMPONENTS_FOLDER, folder, afile)
                            with open(self.json_file, 'r') as json_file:
                                self.parameters = json.load(json_file)
                        if afile.startswith('img'):
                            for f in os.listdir(os.path.join(COMPONENTS_FOLDER, folder, afile)):
                                try:
                                    print('FILE:', f)
                                    image_file_path = os.path.join(COMPONENTS_FOLDER, folder, afile, f)
                                    self.move_file_to_folder(image_file_path, IMAGES_FOLDER)
                                except Exception as e:
                                    print('SOMETHING GO WRONG ', e)

                    #find files by filetypes and move them to django static folders
                    #every file will be renamed to 'name_of_component___filename'
                    self.move_file_to_folder(self.scss_file, SCSS_FOLDER)
                    self.move_file_to_folder(self.js_file, JS_FOLDER)
                    self.update_parameters()
                    self.create_component_object(self.parameters)
                    self.create_lock_file()

    def move_file_to_folder(self, afile, folder):
        try:
            print('moving a file {}'.format(afile))
            #rename a file adding a component name
            old_name = os.path.basename(afile)
            new_name = self.component_title+'__'+old_name
            shutil.move(afile, folder+'/'+new_name)
            # import pdb; pdb.set_trace()
            print('-------->file moved to {}'.format(folder))
        except Exception as e:
            print(e, 'ERROR MOVING A PICT FILE')

    def update_parameters(self):
        scss_file_path = os.path.join(SCSS_FOLDER, os.path.basename(self.scss_file))
        js_file_path = os.path.join(JS_FOLDER, os.path.basename(self.js_file))
        html_file_name = os.path.basename(self.html_file)
        scss_file_name = os.path.basename(self.scss_file)
        js_file_name = os.path.basename(self.js_file)
        self.parameters.update({
            'title': self.component_title,
            'code': self.template_folder_name,
            'html_path': self.html_file,
            'scss_path': scss_file_path,
            'js_path': js_file_path,
            'relative_html_path': TEMPLATE_RELATIVE_FOLDER+html_file_name,
            'relative_scss_path': SCSS_RELATIVE_FOLDER+scss_file_name,
            'relative_js_path': JS_RELATIVE_FOLDER+js_file_name,
        })
        print('***parameters updated: ', self.parameters)

    def create_component_object(self, options):
        component = Component.objects.create(**options)
        print('*** COMPONENT CREATED: ', component.title, component.pk)

    def add_link_to_base_html(self, afile):
        pass

    def create_lock_file(self):
        with open(os.path.join(COMPONENTS_FOLDER, self.template_folder_name, 'installed.lock'), 'w') as f:
            data = "component installed {}".format(self.component_title)
            f.write(data)
            print('done creating lock file')
