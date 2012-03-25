from django.db import models
from wedding.reservations.models import Invitee


class Table(models.Model):
    label = models.CharField(max_length=10, help_text='A short label, used at the venue, to identify a table. Example: "A3", "B1"')
    capacity = models.PositiveIntegerField()
    shape = models.CharField(max_length=10, choices=(
        ('rect', 'Rectangle'),
        ('circle', 'Circle'),
    ))
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('label',)
    
    
class Assignment(models.Model):
    invitee = models.ForeignKey(Invitee)
    table = models.ForeignKey(Table)
    place = models.PositiveIntegerField(help_text='A place number, such that 0 <= n < table.capacity')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('table', 'place')