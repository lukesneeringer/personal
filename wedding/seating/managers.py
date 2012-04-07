from django.db import models


class TableManager(models.Manager):
    def get_query_set(self):
        return super(TableManager, self).get_query_set().prefetch_related('seat_set')