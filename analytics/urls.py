from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='analytics_dashboard'),
    path('track-engagement/', views.track_engagement, name='track_engagement'),
]
