from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class PageView(models.Model):
    path = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40)
    referrer = models.URLField(max_length=500, null=True, blank=True)
    device_type = models.CharField(max_length=20, null=True)  # mobile, tablet, desktop
    browser = models.CharField(max_length=50, null=True)
    os = models.CharField(max_length=50, null=True)
    country = models.CharField(max_length=100, null=True)
    city = models.CharField(max_length=100, null=True)
    is_bounce = models.BooleanField(default=True)  # Will be updated when user views multiple pages

    class Meta:
        indexes = [
            models.Index(fields=['path']),
            models.Index(fields=['timestamp']),
            models.Index(fields=['device_type']),
            models.Index(fields=['country']),
        ]

class UserEngagement(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40)
    page_time = models.IntegerField(help_text="Time spent on page in seconds")
    scroll_depth = models.IntegerField(help_text="Maximum scroll depth in percentage")
    timestamp = models.DateTimeField(default=timezone.now)
    path = models.CharField(max_length=255)
    clicks = models.IntegerField(default=0)
    form_interactions = models.IntegerField(default=0)
    content_shares = models.IntegerField(default=0)
    exit_intent = models.BooleanField(default=False)  # Tracks if user showed exit intent

    class Meta:
        indexes = [
            models.Index(fields=['timestamp']),
            models.Index(fields=['path']),
        ]

class SearchQuery(models.Model):
    query = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now)
    results_count = models.IntegerField()
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40)
    clicked_results = models.IntegerField(default=0)
    successful_search = models.BooleanField(default=False)  # True if user clicked a result

    class Meta:
        indexes = [
            models.Index(fields=['query']),
            models.Index(fields=['timestamp']),
        ]

class UserFlow(models.Model):
    session_key = models.CharField(max_length=40)
    entry_page = models.CharField(max_length=255)
    exit_page = models.CharField(max_length=255, null=True)
    pages_viewed = models.JSONField(default=list)  # List of pages in order
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField(null=True)
    conversion_achieved = models.BooleanField(default=False)
    
    class Meta:
        indexes = [
            models.Index(fields=['session_key']),
            models.Index(fields=['start_time']),
        ]

class ContentInteraction(models.Model):
    content_type = models.CharField(max_length=50)  # blog, service, case-study, etc.
    content_id = models.IntegerField()
    interaction_type = models.CharField(max_length=50)  # view, share, download, etc.
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    session_key = models.CharField(max_length=40)
    timestamp = models.DateTimeField(default=timezone.now)
    time_spent = models.IntegerField(default=0)  # Time spent in seconds
    
    class Meta:
        indexes = [
            models.Index(fields=['content_type', 'content_id']),
            models.Index(fields=['timestamp']),
        ]
