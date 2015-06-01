from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

SOCIAL_NETWORKS = [
    ('twitter',  'Twitter'),
]

class SocialShare(models.Model):
    social_network = models.CharField(max_length=20, choices=SOCIAL_NETWORKS)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
