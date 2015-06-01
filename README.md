django-autosharing
==================

Simple Django app for periodically sharing Django models via social media.

Currently, the app only supports sharing via Twitter.

Installation
------------ 

    pip install git+https://github.com/newsapps/django-autosharing.git

Usage
-----

### Update settings

Make sure `django.contrib.contenttypes` add `autosharing` have been added to your `INSTALLED_APPS` setting:


    INSTALLED_APPS = (
        # django-autocomplete-light has to come before django.contrib.admin
        'autocomplete_light',

        # Django
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',

        # 3rd Party
        'bakery',
        'tribune_omniture.django',
        'storages',
        'easy_thumbnails',
        'autosharing',

        # This project
        'dining',
        'dining_ssor',
        'brightcove',
    )

Generate Twitter OAuth credentials and define the `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN` and `TWITTER_ACCESS_TOKEN_SECRET` Django settings:

    TWITTER_CONSUMER_KEY = os.environ.get('TWITTER_CONSUMER_KEY', None)
    TWITTER_CONSUMER_SECRET = os.environ.get('TWITTER_CONSUMER_SECRET', None)
    TWITTER_ACCESS_TOKEN = os.environ.get('TWITTER_ACCESS_TOKEN', None)
    TWITTER_ACCESS_TOKEN_SECRET = os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', None)

In the previous example we're getting them from environment variables instead of hard-coding them into the Django settings module, though that is fine too, provided you're not publishing your project repository somewhere public.

### Run database migrations

    python manage.py migrate autosharing

### Configure your models

Add a GenericRelation field to any models you want to share:

    from django.contrib.contenttypes.fields import GenericRelation
    from django.db import models
    from autosharing.models import SocialShare

    class Dish(models.Model):
        """A dish or a drink featured in our dining guide"""

        name = models.TextField(help_text='dish or drink name')
        slug = models.SlugField(default='')
        socialshares = GenericRelation(SocialShare)

Make sure the default manager has an `unshared` method that will return any objects that have not been shared.  To use the default implementation, you can do something like this:

    from django.db import models
    from autosharing.query import SharingQuerySetMixin

    class DishQuerySet(SharingQuerySetMixin, models.QuerySet):
        pass

    class Dish(models.Model):
        """A dish or a drink featured in our dining guide"""

        name = models.TextField(help_text='dish or drink name')
        slug = models.SlugField(default='')
        socialshares = GenericRelation(SocialShare)

        objects = DishQuerySet.as_manager()
   
Add a method named `autosharing_tweet` for returning tweet content:

    class Dish(models.Model):
        """A dish or a drink featured in our dining guide"""

        name = models.TextField(help_text='dish or drink name')
        slug = models.SlugField(default='')
        socialshares = GenericRelation(SocialShare)

        objects = DishQuerySet.as_manager()

        def autosharing_tweet(self):
            return self.name + " #lookitsahashtag"


### Share!

You can share a random, previously unshared model using the `autoshare` Django management command:

    python manage.py autoshare dining.Dish twitter
