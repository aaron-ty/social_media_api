from django.urls import path
from .views import (
    PostMessageView, PostPhotoView, PostReelView, 
    PostStoryView, CommentView, PostContentView, InsightsView,
    FacebookCredentialsView
)

urlpatterns = [
    path('api/post_message/', PostMessageView.as_view(), name='post_message'),
    path('api/post_photo/', PostPhotoView.as_view(), name='post_photo'),
    path('api/post_reel/', PostReelView.as_view(), name='post_reel'),
    path('api/post_story/', PostStoryView.as_view(), name='post_story'),
    path('api/comment/', CommentView.as_view(), name='comment'),
    path('api/post_content/', PostContentView.as_view(), name='post_content'),
    path('api/insights/', InsightsView.as_view(), name='insights'),
    path('api/facebook_credentials/', FacebookCredentialsView.as_view(), name='facebook_credentials'),
]
