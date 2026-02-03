from django.core.management.base import BaseCommand
from datetime import timedelta
from django.utils import timezone
from facebook_app.models import FacebookToken, FacebookCredentials
from defines import getCreds, makeApiCall

class Command(BaseCommand):
    help = 'Get and store long-lived Facebook access token'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User ID')
        parser.add_argument('project_id', type=str, help='Project ID')

    def handle(self, *args, **kwargs):
        user_id = kwargs['user_id']
        project_id = kwargs['project_id']
        params = getCreds(user_id, project_id)
        params['debug'] = 'yes'
        response = self.getLongLivedAccessToken(params)

        access_token = response['json_data']['access_token']
        expires_at = timezone.now() + timedelta(days=60)  # Set the expiration date to 60 days from now

        credentials = FacebookCredentials.objects.filter(user_id=user_id, project_id=project_id).latest('created_at')
        
        # Save the access token to the database
        FacebookToken.objects.create(access_token=access_token, expires_at=expires_at, credentials=credentials)

        self.stdout.write(self.style.SUCCESS("Access Token:"))
        self.stdout.write(self.style.SUCCESS(access_token))
        self.stdout.write(self.style.SUCCESS("Access token has been saved to the database"))

    def getLongLivedAccessToken(self, params):
        endpointParams = {
            'grant_type': 'fb_exchange_token',  # tell Facebook we want to exchange token
            'client_id': params['client_id'],  # client id from Facebook app
            'client_secret': params['client_secret'],  # client secret from Facebook app
            'fb_exchange_token': params['access_token']  # access token to get exchanged for a long-lived token
        }

        url = params['endpoint_base'] + 'oauth/access_token'  # endpoint URL

        return makeApiCall(url, endpointParams, params['debug'])  # make the API call
