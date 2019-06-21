from django.core.management.base import BaseCommand
from mainapp.models import SiteConfiguration, Font, Component, ColorScheme
from django.conf import settings
import requests
import json
import random
# import os

# with open(os.path.join(settings.BASE_DIR, 'secret.json'), 'r') as secret_file:
#     secret = json.load(secret_file)
#     ADMIN, PASSWORD, EMAIL = secret['site_admin'], secret['site_admin_password'], secret['site_admin_email']
COLOR_MODES = ['triad', 'analogic-complement']
SEED_COLORS = ['0047AB', '363020', 'E7E247', '4D5061']

class Command(BaseCommand):
    def handle(self, *args, **options):
        ColorScheme.objects.all().delete()
        # get colors from color scheme api
        # create colorscheme objects
        # choose font from existing in database
        # create site_configuration
        # deactivate all site_configurations
        # activate only one configuration
        # Choices: monochrome monochrome-dark monochrome-light analogic complement analogic-complement triad quad
        # address = 'http://www.thecolorapi.com/scheme?hex=0047AB&mode=triad&count=6&format=json'
        for algorythm in COLOR_MODES:
            for seed_color in SEED_COLORS:
                print('****NEW SCHEME****')
                address = 'http://thecolorapi.com/scheme?hex={}&format=json&mode={}&count=5'.format(seed_color, algorythm)
                r = requests.get(address)
                json_request = r.json()
                colors_array = []
                for color in json_request['colors']:
                    print('COLOR', color['hex']['value'])
                    colors_array.append(color['hex']['value'])

                ColorScheme.objects.create(title='SEED_{}'.format(seed_color), colors=','.join(colors_array))
                print('NEW COLORSCHEME CREATED')
        all_colorschemes = ColorScheme.objects.all()
        for color_scheme in all_colorschemes:
            color_scheme.configuration = None
            color_scheme.save()
        random_color_scheme = random.choice([color for color in all_colorschemes])
        configuration = SiteConfiguration.objects.first()
        random_color_scheme.configuration = configuration
        random_color_scheme.save()
        configuration.save()
