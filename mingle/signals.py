from django.db.models.signals import post_save
from django.dispatch import receiver
from otree.models import Session
from .models import MingleSession

@receiver(post_save, sender=Session)
def creating_corresponding_mingle_session(sender, instance, created,  **kwargs):
    if created:
        MingleSession.objects.create(owner=instance)

