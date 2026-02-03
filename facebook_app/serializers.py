from rest_framework import serializers
from .models import FacebookCredentials

class PostMessageSerializer(serializers.Serializer):
    message = serializers.CharField()

class PostPhotoSerializer(serializers.Serializer):
    photo = serializers.ImageField()
    caption = serializers.CharField()

class PostReelSerializer(serializers.Serializer):
    video = serializers.URLField()
    caption = serializers.CharField()

class PostStorySerializer(serializers.Serializer):
    image = serializers.URLField()
    caption = serializers.CharField()

class CommentSerializer(serializers.Serializer):
    post_id = serializers.CharField()
    comment = serializers.CharField()

class PostContentSerializer(serializers.Serializer):
    CONTENT_CHOICES = [
        ('STORIES', 'Story'),
        ('IMAGE', 'Picture'),
        ('REELS', 'Reel'),
    ]
    content_type = serializers.ChoiceField(choices=CONTENT_CHOICES)
    media_url = serializers.URLField()
    caption = serializers.CharField(required=False)

class FacebookCredentialsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FacebookCredentials
        fields = '__all__'
