from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    PostMessageSerializer, PostPhotoSerializer, PostReelSerializer,
    PostStorySerializer, CommentSerializer, PostContentSerializer,
    FacebookCredentialsSerializer  # Ensure this line is correct
)
from .models import FacebookToken, FacebookCredentials
from .facebook_utils import (
    post_photo_to_fb, comment_on_post, get_post_metrics_insights, 
    get_feed, get_page_fan_count, get_page_impressions, 
    get_multiple_insights, get_post_metrics, createMediaObject, 
    getMediaObjectStatus, publishMedia
)
import facebook as fb
import time

def get_access_token(credentials):
    token = FacebookToken.objects.filter(credentials=credentials).latest('created_at')
    return token.access_token

def get_credentials(user_id, project_id):
    credentials = FacebookCredentials.objects.filter(user_id=user_id, project_id=project_id).latest('created_at')
    return credentials

class FacebookCredentialsView(APIView):
    def post(self, request):
        serializer = FacebookCredentialsSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": "Credentials saved successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        user_id = request.query_params.get('user_id')
        project_id = request.query_params.get('project_id')
        if not user_id or not project_id:
            return Response({"error": "user_id and project_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        credentials = get_credentials(user_id, project_id)
        serializer = FacebookCredentialsSerializer(credentials)
        return Response(serializer.data)

class PostMessageView(APIView):
    def post(self, request):
        user_id = request.data.get('user_id')
        project_id = request.data.get('project_id')
        if not user_id or not project_id:
            return Response({"error": "user_id and project_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        serializer = PostMessageSerializer(data=request.data)
        if serializer.is_valid():
            message = serializer.validated_data['message']
            credentials = get_credentials(user_id, project_id)
            graph = fb.GraphAPI(get_access_token(credentials))
            graph.put_object("me", "feed", message=message)
            return Response({"status": "Message posted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PostPhotoView(APIView):
    def post(self, request):
        serializer = PostPhotoSerializer(data=request.data)
        if serializer.is_valid():
            photo = serializer.validated_data['photo']
            caption = serializer.validated_data['caption']
            post_photo_to_fb(photo, caption)
            return Response({"status": "Photo posted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostReelView(APIView):
    def post(self, request):
        serializer = PostReelSerializer(data=request.data)
        if serializer.is_valid():
            video = serializer.validated_data['video']
            caption = serializer.validated_data['caption']
            # Implement logic to post reel to Facebook
            return Response({"status": "Reel posted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostStoryView(APIView):
    def post(self, request):
        serializer = PostStorySerializer(data=request.data)
        if serializer.is_valid():
            image = serializer.validated_data['image']
            caption = serializer.validated_data['caption']
            # Implement logic to post story to Facebook
            return Response({"status": "Story posted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CommentView(APIView):
    def post(self, request):
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            post_id = serializer.validated_data['post_id']
            comment = serializer.validated_data['comment']
            comment_on_post(post_id, comment)
            return Response({"status": "Comment added successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostContentView(APIView):
    def post(self, request):
        serializer = PostContentSerializer(data=request.data)
        if serializer.is_valid():
            content_type = serializer.validated_data['content_type']
            media_url = serializer.validated_data['media_url']
            caption = serializer.validated_data.get('caption', '')

            params = {
                'access_token': get_access_token(),
                'media_type': content_type.upper(),
                'media_url': media_url,
                'caption': caption,
                'endpoint_base': 'https://graph.facebook.com/v19.0'
            }

            media_response = createMediaObject(params)
            media_object_id = media_response['id']
            media_status_code = 'IN_PROGRESS'

            while media_status_code != 'FINISHED':
                status_response = getMediaObjectStatus(media_object_id, params)
                media_status_code = status_response['status_code']
                time.sleep(5)

            publish_response = publishMedia(media_object_id, params)
            return Response({"status": "Content posted successfully!"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class InsightsView(APIView):
    def get(self, request):
        page_id = request.query_params.get('page_id')
        post_id = request.query_params.get('post_id')
        if not page_id or not post_id:
            return Response({"error": "page_id and post_id are required"}, status=status.HTTP_400_BAD_REQUEST)
        
        feed = get_feed(page_id)
        fan_count = get_page_fan_count(page_id)
        impressions = get_page_impressions(page_id)
        metrics = "page_impressions_unique,page_impressions_paid"
        multiple_insights = get_multiple_insights(page_id, metrics)
        post_metrics = "post_reactions_like_total,post_reactions_love_total,post_reactions_wow_total"
        post_metrics_insights = get_post_metrics(post_id, post_metrics)
        
        data = {
            'feed': feed,
            'fan_count': fan_count,
            'impressions': impressions,
            'multiple_insights': multiple_insights,
            'post_metrics_insights': post_metrics_insights,
        }
        return Response(data, status=status.HTTP_200_OK)
