from django.db import models
from mptt.models import (
    MPTTModel,
    TreeForeignKey
)


class Injury(MPTTModel):

    """
    """
    name = models.CharField(max_length=64, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return '{}'.format(self.name)
