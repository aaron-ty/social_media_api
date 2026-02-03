import facebook as fb
import requests
from .models import FacebookToken

def get_access_token():
    token = FacebookToken.objects.latest('created_at')
    return token.access_token

def post_photo_to_fb(photo, caption):
    graph = fb.GraphAPI(get_access_token())
    photo_data = photo.read()
    graph.put_photo(image=photo_data, message=caption)

def comment_on_post(post_id, comment):
    graph = fb.GraphAPI(get_access_token())
    graph.put_comment(object_id=post_id, message=comment)

def get_post_metrics_insights(post_id):
    graph = fb.GraphAPI(get_access_token())
    metrics = "post_reactions_like_total,post_reactions_love_total,post_reactions_wow_total"
    return graph.get_object(id=post_id, fields=metrics)

def get_feed(page_id):
    graph = fb.GraphAPI(get_access_token())
    return graph.get_connections(id=page_id, connection_name='feed')

def get_page_fan_count(page_id):
    graph = fb.GraphAPI(get_access_token())
    return graph.get_object(id=page_id, fields='fan_count')

def get_page_impressions(page_id):
    graph = fb.GraphAPI(get_access_token())
    return graph.get_object(id=page_id, fields='impressions')

def get_multiple_insights(page_id, metrics):
    graph = fb.GraphAPI(get_access_token())
    return graph.get_object(id=page_id, fields=metrics)

def get_post_metrics(post_id, metrics):
    graph = fb.GraphAPI(get_access_token())
    return graph.get_object(id=post_id, fields=metrics)

# Define the createMediaObject function
def createMediaObject(params):
    url = f"{params['endpoint_base']}/{params['media_type'].lower()}s"
    response = requests.post(url, data=params)
    return response.json()

# Define the getMediaObjectStatus function
def getMediaObjectStatus(media_object_id, params):
    url = f"{params['endpoint_base']}/{media_object_id}"
    response = requests.get(url, params=params)
    return response.json()

# Define the publishMedia function
def publishMedia(media_object_id, params):
    url = f"{params['endpoint_base']}/{media_object_id}/publish"
    response = requests.post(url, data=params)
    return response.json()
