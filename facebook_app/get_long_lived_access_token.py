import os
import django
from datetime import timedelta
from django.utils import timezone

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'facebook_api.settings')
django.setup()

from facebook_app.models import FacebookToken
from defines import getCreds, makeApiCall

def getLongLivedAccessToken(params):
    """ Get long-lived access token
    
    API Endpoint:
        https://graph.facebook.com/{graph-api-version}/oauth/access_token?grant_type=fb_exchange_token&client_id={app-id}&client_secret={app-secret}&fb_exchange_token={your-access-token}

    Returns:
        object: data from the endpoint
    """
    endpointParams = {
        'grant_type': 'fb_exchange_token',  # tell Facebook we want to exchange token
        'client_id': params['client_id'],  # client id from Facebook app
        'client_secret': params['client_secret'],  # client secret from Facebook app
        'fb_exchange_token': params['access_token']  # access token to get exchanged for a long-lived token
    }

    url = params['endpoint_base'] + 'oauth/access_token'  # endpoint URL

    return makeApiCall(url, endpointParams, params['debug'])  # make the API call

if __name__ == "__main__":
    params = getCreds()
    params['debug'] = 'yes'
    response = getLongLivedAccessToken(params)

    access_token = response['json_data']['access_token']
    expires_at = timezone.now() + timedelta(days=60)  # Set the expiration date to 60 days from now

    # Save the access token to the database
    FacebookToken.objects.create(access_token=access_token, expires_at=expires_at)

    print("\n ---- ACCESS TOKEN INFO ----\n")
    print("Access Token:")
    print(access_token)
    print("\nAccess token has been saved to the database")
