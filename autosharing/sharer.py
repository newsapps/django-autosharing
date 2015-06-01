import logging

import tweepy

from django.conf import settings

from .models import SocialShare


logger = logging.getLogger('autosharing')

class Sharer(object):
    def message_for_object(self, o):
        raise NotImplemented

    def share(self, o, dry_run):
        raise NotImplemented

    def record_share(self, o):
        ss = SocialShare(content_object=o, social_network=self.social_network)
        ss.save()


class TwitterSharer(Sharer):
    social_network = 'twitter'

    def __init__(self):
        auth = tweepy.OAuthHandler(
            settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(
            settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        self._twitter_api = tweepy.API(auth)

    def message_for_object(self, o):
        return o.autosharing_tweet()

    def share(self, o, dry_run=False):
        msg = self.message_for_object(o)
        logger.debug('Sharing tweet "{}"'.format(msg))
        if dry_run:
            return

        try:
            self._twitter_api.update_status(status=msg)
            self.record_share(o)
        except tweepy.error.TweepError as e:
            print('Error sharing tweet: "{}": {}'.format(msg, e))
            import traceback
            traceback.print_exc()
            logger.error('Error sharing tweet: "{}": {}'.format(msg, e))



SHARERS = {
    'twitter': TwitterSharer,      
}

def get_sharer(social_network):
    return SHARERS[social_network]()
