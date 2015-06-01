from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db.models import Count


class SharingQuerySetMixin(object):
    def _get_sharing_field(self):
        from autosharing.models import SocialShare

        for field in self.model._meta.virtual_fields:
            if (isinstance(field, GenericRelation) and
                    field.related_model == SocialShare):
                return field
        else:
            msg = ("Could not find generic relation field to SocialShare "
                    " on model {}").format(self.model.name)
            raise ValueError(msg)
           
    def unshared(self, max_shares=0):
        share_field_name = self._get_sharing_field().name
        ctype = ContentType.objects.get_for_model(self.model)
        filter_kwargs = {
            share_field_name + '__content_type': ctype
        }
        qs = self.filter(**filter_kwargs)
        qs = self.annotate(num_social_shares=Count(share_field_name))
        return qs.filter(num_social_shares__lte=max_shares)
