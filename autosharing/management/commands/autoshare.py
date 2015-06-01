from random import randint

from django.apps import apps
from django.core.management import BaseCommand

from autosharing.sharer import get_sharer

class Command(BaseCommand):
    help = 'Share a Django model instance via social media'

    def add_arguments(self, parser):
        parser.add_argument('model_path',
            action='store',
            help='Dotted class of Django model (appname.ModelName) to share')
        parser.add_argument('social_network',
            action='store',
            help="Name of social network for sharing")
        parser.add_argument('--dry-run',
            action='store_true',
            dest='dry_run',
            default=False,
            help="Don't actually post the message"
        )

    def get_unshared_model(self, model_cls):   
        unshared_count = model_cls.objects.unshared().count()
        random_index =  randint(0, unshared_count - 1)
        return model_cls.objects.unshared()[random_index]
   
    def handle(self, model_path, social_network, *args, **options):
        app_label, model_name = model_path.split('.')
        dry_run = options['dry_run']
        model_cls = apps.get_model(app_label, model_name)
        model = self.get_unshared_model(model_cls)
        sharer = get_sharer(social_network) 
        sharer.share(model, dry_run)
