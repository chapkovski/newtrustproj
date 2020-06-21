from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from otree.models import Session, Participant
from .models import MingleSession, MegaSession, MegaParticipant, MegaGroup
from trust.models import City


@receiver(post_save, sender=Session)
def creating_corresponding_mingle_session(sender, instance, created, **kwargs):
    """Here insert the logic so only 'right' sessions will have mingle counterparts
    (those with Trust app, toloka pool id, etc)"""
    if created:
        apps = instance.config['app_sequence']
        city_code = instance.config.get('city_code')

        if 'trust' in apps and city_code:
            try:
                city = City.objects.get(code=city_code)
                MingleSession.objects.create(owner=instance, city=city)
            except City.DoesNotExist:
                #TODO logger
                print('city does not exist', city_code)


@receiver(post_save, sender=MingleSession)
def monitoring_mingle_sessions(sender, instance, created, **kwargs):
    """Monitoring changes in mingle session belonging and delete empty
    megasessions which have not mingle sessions in it"""
    MegaSession.objects.filter(minglesessions__isnull=True).delete()
    """for any change in mingle session we check - if a megaparticipant for the 
    owner exists. Is it a safe way? if megaparticipant for participant already exists then 
    it can cause an error. On the other hand we may clean all existing megaparticipants?
    but what if they are already the part  of some megagroups?
    """

    participants = Participant.objects.filter(session=instance.owner)
    megapars = [MegaParticipant(owner=i, megasession=instance.megasession, city=instance.city) for i in participants]
    MegaParticipant.objects.bulk_create(megapars)


@receiver(post_save, sender=MegaParticipant)
def cleaning_empty_groups(sender, instance, **kwargs):
    """Monitoring changes in megaparticipants belonging and delete empty
        megagroups which have no participants."""
    MegaGroup.objects.filter(megaparticipants__isnull=True).delete()
