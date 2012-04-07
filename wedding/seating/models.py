from django.db import models
from wedding.reservations.models import RSVP
from wedding.seating import managers


class Table(models.Model):
    """A model representing a table within a scheme."""
    
    objects = managers.TableManager()
    
    label = models.CharField(max_length=10, help_text='A short label, used at the venue, to identify a table. Example: "A1", "B4"')
    description = models.CharField(max_length=255, help_text='A human-readable description of who is being placed at this table. Example: "RotD", "Meagan\'s Family - Maternal"')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('label',)
    
    def __unicode__(self):
        return '%s (%s)' % (self.label, self.description)
        
    def __nonzero__(self):
        return True
        
    def __len__(self):
        return len(self.seat_set.all())
        
        
class Seat(models.Model):
    """A model representing a seat at a table, occupied by
    an invitee who is coming to the wedding."""
    
    person = models.OneToOneField(RSVP, limit_choices_to={
        'accepts': True,
    })
    table = models.ForeignKey(Table)
    position = models.PositiveIntegerField(help_text='A position at a table, zero-indexed. Tables are assumed to be circular; seat 0 is adjacent to seat N - 1 (where N is the table\'s capacity).')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('table', 'position')
        
    def __unicode__(self):
        return '%s(%d): %s' % (self.table.label, self.position, self.person)