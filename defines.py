import requests
import json
from facebook_app.models import FacebookCredentials, FacebookToken

def getCreds(user_id, project_id):
    """ Get creds required for use in the applications
    
    Returns:
        dictionary: credentials needed globally
    """
    creds = dict() # dictionary to hold everything
    credentials = FacebookCredentials.objects.filter(user_id=user_id, project_id=project_id).latest('created_at')
    creds['access_token'] = credentials.access_token
    creds['client_id'] = credentials.client_id
    creds['client_secret'] = credentials.client_secret
    creds['graph_domain'] = 'https://graph.facebook.com/' # base domain for api calls
    creds['graph_version'] = 'v19.0' # version of the api we are hitting
    creds['endpoint_base'] = creds['graph_domain'] + creds['graph_version'] + '/' # base endpoint with domain and version
    creds['debug'] = 'no' # debug mode for api call
    creds['page_id'] = credentials.page_id
    creds['instagram_account_id'] = credentials.instagram_account_id
    creds['ig_username'] = credentials.ig_username

    return creds

def makeApiCall(url, endpointParams, debug='no'):
    """ Request data from endpoint with params
    
    Args:
        url: string of the url endpoint to make request from
        endpointParams: dictionary keyed by the names of the url parameters

    Returns:
        object: data from the endpoint
    """
    data = requests.get(url, endpointParams) # make get request

    response = dict() # hold response info
    response['url'] = url # url we are hitting
    response['endpoint_params'] = endpointParams #parameters for the endpoint
    response['endpoint_params_pretty'] = json.dumps(endpointParams, indent=4) # pretty print for cli
    response['json_data'] = json.loads(data.content) # response data from the api
    response['json_data_pretty'] = json.dumps(response['json_data'], indent=4) # pretty print for cli

    if debug == 'yes': # display out response info
        displayApiCallData(response) # display response

    return response # get and return content

def displayApiCallData(response):
    """ Print out to cli response from api call """

    print("\nURL: ")  # title
    print(response['url'])  # display url hit
    print("\nEndpoint Params: ")  # title
    print(response['endpoint_params_pretty'])  # display params passed to the endpoint
    print("\nResponse: ")  # title
    print(response['json_data_pretty'])  # make look pretty for cli
