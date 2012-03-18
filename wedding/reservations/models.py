# encoding: utf-8
from django.contrib.auth.models import User
from django.db import models
from tools.decorators import cached_property
from wedding.reservations import managers


class Invitation(models.Model):
    """A single invitation sent to a family at a given address."""
    
    objects = managers.InvitationManager()
    
    user = models.OneToOneField(User, null=True, blank=True)
    token = models.CharField(max_length=8, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    rehearsal_dinner = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.formal_name
        
    def __len__(self):
        return self.invitee_set.count()
        
    def __nonzero__(self):
        return True
        
    @cached_property
    def primary_last_name(self):
        """Return the primary last name for this invitation. Used
        for ordering within the admin."""
        return self.adults[0].last_name
        
    @cached_property
    def formal_name(self):
        """Return the formal name used to address this invitation."""
        
        # if there is only one adult, use the adult's formal name
        if len(self.adults) == 1:
            return unicode(self.adults[0])
            
        # okay, there are two adults -- if their last names match,
        # then we want a single, unified format
        # (e.g. "Mr. & Mrs. Jonathan Chappell")
        if self.adults[0].last_name == self.adults[1].last_name:
            return u'%(male_title)s & %(female_title)s %(male_first_name)s %(last_name)s' % {
                'female_title': self.adults[1].title,
                'last_name': self.adults[0].last_name,
                'male_title': self.adults[0].title,
                'male_first_name': self.adults[0].first_name,
            }
            
        # okay, the last names don't match; print the names out separately
        # and in their entirety
        # (e.g. "Mr. Daniel Beltz and Miss Jessica Dymer")
        return u'%s & %s' % (self.adults[0], self.adults[1])
        
    @cached_property
    def informal_name(self):
        """Return a less formal version of the names of the adults
        on this invitation."""
        
        # if there is only one adult, use the adult's first and last name
        if len(self.adults) == 1:
            return u'%s %s' % (self.adults[0].first_name, self.adults[0].last_name)
            
        # okay, there are two adults -- if their last names match,
        # then return a single format with both informal first names but the shared
        # last name (e.g. "Jon and Andi Chappell")
        if self.adults[0].last_name == self.adults[1].last_name:
            return u'%(male_first_name)s & %(female_first_name)s %(last_name)s' % {
                'female_first_name': self.adults[1].nickname,
                'male_first_name': self.adults[0].nickname,
                'last_name': self.adults[0].last_name,
            }
            
        # okay, there are two adults with different last names; print
        # them out separately but with no titles
        # (e.g. "Dan Beltz & Jess Dymer")
        return u'%(male_first_name)s %(male_last_name)s & %(female_first_name)s %(female_last_name)s' % {
            'female_first_name': self.adults[1].nickname,
            'female_last_name': self.adults[1].last_name,
            'male_first_name': self.adults[0].nickname,
            'male_last_name': self.adults[0].last_name,
        }    
    
    @cached_property
    def adults(self):
        return self.invitee_set.order_by('-sex', 'last_name', 'first_name').filter(age_group='adult')
        
    @cached_property
    def youths(self):
        return self.invitee_set.order_by('last_name', 'first_name').filter(age_group='adult_')
        
    @cached_property
    def children(self):
        return self.invitee_set.order_by('last_name', 'first_name').filter(age_group='child')
        
    @cached_property
    def infants(self):
        return self.invitee_set.order_by('last_name', 'first_name').filter(age_group__in=('free', 'infants'))
        
    @cached_property
    def attending(self):
        """Return True if anyone on this invitation is attending,
        False if nobody is attending.
        If we have not yet received a response, return None.
        """
        
        rsvps = RSVP.objects.filter(invitee__invitation=self)
        if len(rsvps) == 0:
            return None
        return reduce(lambda x, y: x | y, [i.accepts for i in rsvps])
        
    
class Invitee(models.Model):
    """A specific person invited included on an invitation."""
    
    invitation = models.ForeignKey(Invitation)
    title = models.CharField(max_length=16)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    nickname = models.CharField(max_length=16, blank=True, help_text='An informal or short name, if the person uses one (e.g. "Elli", "Jon").')
    age_group = models.CharField(
        choices=(
            ('adult', 'Adult (10+) - Primary Addressee'),
            ('adult_', 'Adult (10+) - Not Primary Addressee'),
            ('child', 'Child (5 - 10 years)'),
            ('free', 'Small Child (2 - 5 years)'),
            ('infant', 'Infant (0 - 23 months)'),
        ),
        default='adult',
        db_index=True,
        help_text='The age group of the invitee. This affects how the invitation is "named", as only adults are primary names on the invitation, as well as pricing information sent to the venue. Note: Each invitation must have exactly one or two primary residents; not zero, not 3+.',
        max_length=6,
    )
    sex = models.CharField(max_length=6, choices=(
        ('male', 'Male'),
        ('female', 'Female'),
    ), db_index=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('last_name', 'first_name')
    
    def __unicode__(self):
        return '%s %s %s' % (self.title, self.first_name, self.last_name)
        
    def get_rsvp_form(self, post=None):
        from wedding.reservations.forms import RSVPForm, InfantRSVPForm
        if self.age_group == 'infant':
            return InfantRSVPForm(post, instance=self.reservation, prefix=hash(unicode(self)))
        return RSVPForm(post, instance=self.reservation, prefix=hash(unicode(self)))
        
    @cached_property
    def reservation(self):
        try:
            return self.rsvp
        except RSVP.DoesNotExist:
            return RSVP(invitee=self)
    

class RSVP(models.Model):
    """A response from an individual on whether they will attend,
    and their food order."""
    
    invitee = models.OneToOneField(Invitee, related_name='rsvp')
    accepts = models.BooleanField(default=True, verbose_name='attending', choices=(
        (True, 'Accepts'),
        (False, 'Regrets'),
    ))
    food = models.CharField(max_length=16, choices=(
        ('chicken', 'Chicken'),
        ('fish', 'Fish'),
        ('steak', 'Steak'),
        ('vegetarian', 'Vegetarian'),
        ('gluten-free', 'Gluten Free'),
    ), null=True, blank=True, verbose_name='entreé')
    medium = models.CharField(max_length=10, choices=(
        ('mail', 'Mail'),
        ('online', 'Online'),
        ('verbal', 'Verbal'),
    ), help_text='The response medium this person used.', default='mail')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ('invitee',)
        verbose_name = 'RSVP'
        
    def __unicode__(self):
        return u'RSVP: %s' % self.invitee
    

class Gift(models.Model):
    """A mapping between an invitation and the gift we received from
    the invitees. For thank you notes."""
    
    invitation = models.ForeignKey(Invitation)
    label = models.CharField(max_length=250, help_text='A terse statement of "what this gift is". For instance, "linen sheets", "gaming table".')
    notes = models.TextField(blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    
    def __unicode__(self):
        return self.label
        
        
from wedding.reservations.signals import *