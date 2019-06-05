# from django.core.signals import request_finished
from django.db.models.signals import pre_save
from django.dispatch import receiver
from mainapp.models import Component


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
