from django.db import models

class InvitationManager(models.Manager):
    def get_query_set(self):
        return super(InvitationManager, self).get_query_set().distinct().prefetch_related('invitee_set')