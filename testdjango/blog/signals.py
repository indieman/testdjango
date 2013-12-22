__author__ = 'indieman'

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from models import Hashtag


@receiver(pre_save, sender=Hashtag)
def get_colors_bags(sender, instance, **kwargs):
    instance.name = '_'.join(instance.name.split())
