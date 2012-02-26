from django.dispatch import receiver
from django.db.models.signals import pre_save
from random import choice
from wedding.reservations.models import Invitation, Invitee


@receiver(pre_save, sender=Invitation)
def on_invitation_save(sender, instance, **kwargs):
    if not instance.token:
        instance.token = ''.join([choice('23456789abcdefghjkmnpqrstuvwxyz') for i in range(0,8)])
        
@receiver(pre_save, sender=Invitee)
def on_invitee_save(sender, instance, **kwargs):
    if not instance.nickname:
        instance.nickname = instance.first_name