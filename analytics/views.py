from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Count, Avg, Sum
from django.utils import timezone
from datetime import timedelta
from django.db.models.functions import TruncDate, TruncHour
from core.models import ContactMessage, Service
from blog.models import Post
from .models import PageView, UserEngagement, SearchQuery, UserFlow, ContentInteraction
import redis
from django.conf import settings
import json
from django.http import HttpResponseForbidden, HttpResponse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import logging

logger = logging.getLogger(__name__)

class DashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'analytics/dashboard.html'
    login_url = '/admin/login/'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def handle_no_permission(self):
        if not self.request.user.is_authenticated:
            return super().handle_no_permission()
        return HttpResponseForbidden("You don't have permission to access this page.")
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.now()
        last_30_days = now - timedelta(days=30)
        last_24_hours = now - timedelta(hours=24)
        last_7_days = now - timedelta(days=7)
        
        # Connect to Redis
        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0)
        
        # Real-time stats from Redis
        try:
            context['active_users'] = int(r.get('active_users') or 0)
            context['current_page_views'] = int(r.get('current_page_views') or 0)
        except (redis.RedisError, TypeError, ValueError) as e:
            context['active_users'] = 0
            context['current_page_views'] = 0

        # Overall Traffic Metrics
        total_views = PageView.objects.filter(timestamp__gte=last_30_days).count()
        unique_visitors = PageView.objects.filter(timestamp__gte=last_30_days).values('session_key').distinct().count()
        bounce_sessions = PageView.objects.filter(timestamp__gte=last_30_days, is_bounce=True).values('session_key').distinct().count()
        
        context['traffic_overview'] = {
            'total_views': total_views,
            'unique_visitors': unique_visitors,
            'bounce_rate': (bounce_sessions / unique_visitors * 100) if unique_visitors > 0 else 0,
        }
        
        # Device Statistics
        device_stats = PageView.objects.filter(
            timestamp__gte=last_30_days
        ).values('device_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        context['device_stats'] = device_stats
        
        # Geographic Distribution
        geo_stats = PageView.objects.filter(
            timestamp__gte=last_30_days
        ).values('country').annotate(
            visits=Count('id')
        ).order_by('-visits')[:10]
        
        context['geo_stats'] = geo_stats
        
        # User Flow Analysis
        user_flows = UserFlow.objects.filter(
            start_time__gte=last_7_days,
            conversion_achieved=True
        ).values('pages_viewed')[:100]
        
        # Aggregate common paths
        conversion_paths = {}
        for flow in user_flows:
            path = ' -> '.join(flow['pages_viewed'])
            conversion_paths[path] = conversion_paths.get(path, 0) + 1
        
        context['top_conversion_paths'] = dict(
            sorted(conversion_paths.items(), key=lambda x: x[1], reverse=True)[:5]
        )
        
        # Content Performance
        content_stats = ContentInteraction.objects.filter(
            timestamp__gte=last_30_days
        ).values('content_type', 'content_id').annotate(
            views=Count('id'),
            avg_time=Avg('time_spent'),
            shares=Count('id', filter=Q(interaction_type='share'))
        ).order_by('-views')[:10]
        
        context['content_performance'] = content_stats
        
        # User Engagement Metrics
        engagement_stats = UserEngagement.objects.filter(
            timestamp__gte=last_30_days
        ).aggregate(
            avg_time=Avg('page_time'),
            avg_scroll=Avg('scroll_depth'),
            avg_clicks=Avg('clicks'),
            form_interactions=Sum('form_interactions'),
            content_shares=Sum('content_shares'),
            exit_intents=Count('id', filter=Q(exit_intent=True))
        )
        
        context['engagement_stats'] = engagement_stats
        
        # Search Analytics
        search_stats = SearchQuery.objects.filter(
            timestamp__gte=last_30_days
        ).aggregate(
            total_searches=Count('id'),
            successful_searches=Count('id', filter=Q(successful_search=True)),
            avg_results=Avg('results_count'),
            avg_clicks=Avg('clicked_results')
        )
        
        context['search_stats'] = search_stats
        
        # Hourly Traffic Pattern
        hourly_traffic = PageView.objects.filter(
            timestamp__gte=last_7_days
        ).annotate(
            hour=TruncHour('timestamp')
        ).values('hour').annotate(
            views=Count('id')
        ).order_by('hour')
        
        context['hourly_traffic'] = list(hourly_traffic)
        
        # Entry and Exit Pages
        entry_pages = PageView.objects.filter(
            timestamp__gte=last_30_days
        ).values('path').annotate(
            entries=Count('id', filter=Q(referrer__isnull=True))
        ).order_by('-entries')[:5]
        
        exit_pages = UserFlow.objects.filter(
            start_time__gte=last_30_days,
            exit_page__isnull=False
        ).values('exit_page').annotate(
            exits=Count('id')
        ).order_by('-exits')[:5]
        
        context['entry_exit_pages'] = {
            'entry_pages': entry_pages,
            'exit_pages': exit_pages
        }
        
        return context

@csrf_exempt
@require_POST
def track_engagement(request):
    try:
        data = json.loads(request.body)
        UserEngagement.objects.create(
            user=request.user if request.user.is_authenticated else None,
            session_key=request.session.session_key,
            page_time=data.get('page_time', 0),
            scroll_depth=data.get('scroll_depth', 0),
            path=data.get('path', ''),
            clicks=data.get('clicks', 0),
            form_interactions=data.get('form_interactions', 0)
        )
        return HttpResponse(status=201)
    except Exception as e:
        logger.error(f"Error tracking engagement: {e}")
        return HttpResponse(status=400)
