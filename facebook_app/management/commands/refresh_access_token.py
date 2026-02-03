from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from facebook_app.models import FacebookToken
from facebook_app.defines import getCreds, makeApiCall

class Command(BaseCommand):
    help = 'Refresh Facebook access token'

    def handle(self, *args, **kwargs):
        params = getCreds()
        params['debug'] = 'yes'
        response = self.getLongLivedAccessToken(params)

        access_token = response['json_data']['access_token']
        expires_at = timezone.now() + timedelta(days=60)  # Set the expiration date to 60 days from now

        # Save the access token to the database
        FacebookToken.objects.create(access_token=access_token, expires_at=expires_at)

        self.stdout.write(self.style.SUCCESS("Access Token:"))
        self.stdout.write(self.style.SUCCESS(access_token))
        self.stdout.write(self.style.SUCCESS("Access token has been refreshed and saved to the database"))

    def getLongLivedAccessToken(self, params):
        endpointParams = {
            'grant_type': 'fb_exchange_token',  # tell Facebook we want to exchange token
            'client_id': params['client_id'],  # client id from Facebook app
            'client_secret': params['client_secret'],  # client secret from Facebook app
            'fb_exchange_token': params['access_token']  # access token to get exchanged for a long-lived token
        }

        url = params['endpoint_base'] + 'oauth/access_token'  # endpoint URL

        return makeApiCall(url, endpointParams, params['debug'])  # make the API call
