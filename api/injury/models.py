from django.db import models
from modeltranslation.utils import auto_populate
from mptt.models import (
    MPTTModel,
    TreeForeignKey
)


class Injury(MPTTModel):

    """
    """
    name = models.CharField(default='', max_length=64, unique=True)
    parent = TreeForeignKey('self', null=True, blank=True, related_name='children', db_index=True)

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return '{}'.format(self.name)


# from modeltranslation.utils import auto_populate
#
# with auto_populate():
#    x = News.objects.create(title='bar')
#
# this will auto fill other language title field with 'bar'
