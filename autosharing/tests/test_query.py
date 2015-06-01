from django.test import TestCase

from autosharing.models import SocialShare
from .models import TestModel


class TestSharingQuerysetMixin(TestCase):
    def test_unshared(self):
        m1 = TestModel.objects.create(name="one")
        m2 = TestModel.objects.create(name="two")
        self.assertEqual(TestModel.objects.unshared().count(), 2)
        ss = SocialShare(content_object=m1, social_network='twitter')
        ss.save()
        self.assertEqual(TestModel.objects.unshared().count(), 1)
        self.assertEqual(TestModel.objects.unshared()[0], m2)
        
