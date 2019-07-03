# from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from mainapp.models import Component, ColorScheme, SiteConfiguration
from django.shortcuts import get_object_or_404
from colour import Color
from django.utils.termcolors import colorize
from django.conf import settings
import shutil, os, subprocess


# @receiver(pre_save, sender=Component)
# def my_callback(sender, **kwargs):
#     print('------------->PRE_SAVE SIGNAL RICIEVED from {}'.format(sender))

@receiver(post_save, sender=ColorScheme)
def update_configuration_colors(sender, instance, **kwargs):
    # print('------------->post_save reciever: {}'.format(instance))
    if instance.configuration:
        #check other schemes
        #save configuration to update scss variables
        other_schemes = ColorScheme.objects.all().exclude(pk=instance.pk)
        for scheme in other_schemes:
            if scheme.configuration:
                scheme.configuration = None
                scheme.save()
        configuration = instance.configuration
        configuration.save()
        static_path = os.path.join(settings.BASE_DIR, 'static_root', 'scss')
        assets_path = os.path.join(settings.BASE_DIR, 'assets', 'scss')
        if settings.DEBUG is True:
            for r, d, f in os.walk(assets_path):
                for file in f:
                    if file in ['component.css', 'component.css.map', 'style.css', 'style.css.map']:
                        # /home/popov/ac_template_site/static_root/scss/components/info-block-v1/component.css
                        src_path = os.path.join(r, file)
                        dst_path = src_path.replace('assets', 'static_root')
                        if os.path.isfile(dst_path):
                            print('it is here', file)
                            os.remove(dst_path)
                            shutil.copy(src_path, dst_path)
                            print('replaced')

        # src_file = os.path.join(settings.BASE_DIR, 'assets', 'scss', '_variables.scss')
        # dst_file = os.path.join(settings.BASE_DIR, 'static_root', 'scss', '_variables.scss')
        # if os.path.isfile(dst_file):
        #     os.remove(dst_file)
        #     shutil.copy(src_file, dst_file)
        #     subprocess.run(['python3', 'manage.py', 'collectstatic', '--noinput'])

        # print('POST_SAVE SIGNAL -> CONFIGURATION {} UPDATED'.format(configuration))

# @receiver(pre_save, sender=SiteConfiguration)
@receiver(post_save, sender=SiteConfiguration)
def callback(sender, instance, **kwargs):
    # print('---->callback configuration')
    # print(sender.color_set.__get__(instance))
    # components = Component.objects.filter(configuration=instance.pk)
    if instance.activated:
        colorscheme = ColorScheme.objects.get(configuration=instance.pk)
        site_colors = [color.strip() for color in colorscheme.colors.split(",")]
        site_colors_pseudo_names = ['$primary', '$secondary', '$neutral',
            '$background', '$highlight']
        color_dict = dict(map(lambda *args: args, site_colors_pseudo_names, site_colors))
        for colr in site_colors:
            colr_obj = Color(colr)
            if colr_obj.luminance >= 0.2:
                darker_luminance = colr_obj.luminance - 0.2
            else:
                darker_luminance = 0
            if colr_obj.luminance <=0.8:
                lighter_luminance = colr_obj.luminance + 0.2
            else:
                lighter_luminance = 1
            darker_color = Color(colr, luminance=darker_luminance)
            color_dict.update(
                {'{}Dark'.format(site_colors_pseudo_names[site_colors.index(colr)]): darker_color.hex_l}
            )
            lighter_color = Color(colr, luminance=lighter_luminance)
            color_dict.update(
                {'{}Light'.format(site_colors_pseudo_names[site_colors.index(colr)]): lighter_color.hex_l}
            )
        with open(instance.color_set_path, 'w') as color_set_file:
            data = []
            for key, value in color_dict.items():
                data.append("{}: {};\n".format(key, value))
            color_set_file.writelines(data)
            # print(colorize('COLORSCHEME VARIABLES UPDATED', bg='blue'))

