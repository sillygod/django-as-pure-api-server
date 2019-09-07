from django.db import models
from django.conf import settings

from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation


class Message(models.Model):
    """a message model
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             models.CASCADE,
                             related_name='messages')

    # for generic foreign key usage
    content_type = models.ForeignKey(ContentType,
                                     blank=True,
                                     null=True,
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField(blank=True, null=True)

    subject = GenericForeignKey('content_type', 'object_id')
    replies = GenericRelation('Message')
    message = models.TextField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)
