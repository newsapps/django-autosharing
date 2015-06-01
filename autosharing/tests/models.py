from django.contrib.contenttypes.fields import GenericRelation
from django.db import models

from autosharing.models import SocialShare
from autosharing.query import SharingQuerySetMixin 


class TestModelQuerySet(SharingQuerySetMixin, models.QuerySet):
    pass


class TestModel(models.Model):
    name = models.CharField(max_length=100)
    socialshares = GenericRelation(SocialShare) 

    objects = TestModelQuerySet.as_manager()
