from django.db import models
from django.contrib.auth.models import User

class FacebookCredentials(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_id = models.CharField(max_length=100)
    access_token = models.TextField()
    client_id = models.CharField(max_length=100)
    client_secret = models.CharField(max_length=100)
    page_id = models.CharField(max_length=100)
    instagram_account_id = models.CharField(max_length=100)
    ig_username = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.ig_username}"

class FacebookToken(models.Model):
    credentials = models.ForeignKey(FacebookCredentials, on_delete=models.CASCADE, default=1)  # Replace '1' with an appropriate default value
    access_token = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def __str__(self):
        return self.access_token
