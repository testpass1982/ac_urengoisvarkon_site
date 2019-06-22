# from django.core.signals import request_finished
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from mainapp.models import Component, ColorScheme, SiteConfiguration
from django.shortcuts import get_object_or_404
from colour import Color
from django.utils.termcolors import colorize


def check_it():
    print('CHEKIT WORKING')


@receiver(pre_save, sender=Component)
def my_callback(sender, **kwargs):
    print('------------->SIGNAL RICIEVED from {}'.format(sender))

@receiver(pre_save, sender=Component)
def make_template(sender, **kwargs):
    print('------------->ME TOO')
    # find template files in components folder
    # place component.css file in static folder
    # place component.html in template folder
    # add link:css in <head> of base.html
    # place include in the right place of base.html
    pass

# @receiver(pre_save, sender=ColorScheme)
# def callback(sender, **kwargs):
#     print('---->callback colorscheme')

@receiver(post_save, sender=ColorScheme)
def update_configuration_colors(sender, instance, **kwargs):
    # import pdb; pdb.set_trace()
    print('--------------------->callback colorscheme')
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
        print('POST_SAVE CONFIGURATION UPDATED', configuration)
    
@receiver(pre_save, sender=SiteConfiguration)
def callback(sender, instance, **kwargs):
    # print('---->callback configuration')
    # print(sender.color_set.__get__(instance))
    try:
        colorscheme = ColorScheme.objects.get(configuration=instance.pk)
    except Exception as e:
        print('ERROR', e)
    # components = Component.objects.filter(configuration=instance.pk)
    if instance.activated:
        site_colors = [color.strip() for color in colorscheme.colors.split(",")]
        site_pseudo_names = ['$primary', '$secondary', '$neutral',
            '$background', '$highlight']
        color_dict = dict(map(lambda *args: args, site_pseudo_names, site_colors))
        for colr in site_colors:
            colr_obj = Color(colr)
            # print('LUMINANCE', colr_obj, colr_obj.luminance)
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
                {'{}Dark'.format(site_pseudo_names[site_colors.index(colr)]): darker_color.hex_l}
            )
            lighter_color = Color(colr, luminance=lighter_luminance)
            color_dict.update(
                {'{}Light'.format(site_pseudo_names[site_colors.index(colr)]): lighter_color.hex_l}
            )
        with open(instance.color_set_path, 'w') as color_set_file:
            data = []
            for key, value in color_dict.items():
                data.append("{}: {};\n".format(key, value))
            color_set_file.writelines(data)
            print(colorize('COLORSCHEME VARIABLES UPDATED', bg='blue'))

