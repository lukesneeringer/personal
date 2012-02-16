from django.db import models


class Invitation(models.Model):
    """A single invitation sent to a family at a given address."""
    
    user = models.ForeignKey(User, null=True, blank=True)
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip_code = models.CharField(max_length=5)
    rehearsal_dinner = models.BooleanField(default=False)
    
    @property
    def formal_name(self):
        """Return the formal name used to address this invitation."""
    
    @property
    def adults(self):
        return self.invitee_set.filter(age_group='adult')
        
    @property
    def children(self):
        return self.invitee_set.filter(age_group='children')
        
    @property
    def infants(self):
        return self.invitee_set.filter(age_group='infants')
        
    
class Invitee(models.Model):
    """A specific person invited included on an invitation."""
    
    title = models.CharField(max_length=16)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age_group = models.CharField(max_length=6, choices=(
        ('adult', 'Adult'),
        ('child', 'Child (2 - 16 years)'),
        ('infant', 'Infant (0 - 23 months)'),
    ), default='adult')
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    

class RSVP(models.Model):
    """A response from an individual on whether they will attend,
    and their food order."""
    
    invitee = models.OneToOneField(Invitee, related_name='rsvp')
    accepts = models.BooleanField(default=True)
    food = models.CharField(max_length=16, choices=(
        ('chicken', 'Chicken'),
        ('fish', 'Fish'),
        ('steak', 'Steak'),
        ('vegetarian', 'Vegetarian')
        ('gluten-free', 'Gluten Free'),
    ), null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)