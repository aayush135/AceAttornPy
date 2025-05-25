from django.contrib import admin
from django.core.cache import cache
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from core.models import ContactMessage, Service
from blog.models import Post

class DashboardAdmin(admin.AdminSite):
    site_header = 'AceAttorn Legal Solutions Admin'
    site_title = 'AceAttorn Admin Portal'
    index_title = 'Dashboard'
    
    def get_app_list(self, request):
        app_list = super().get_app_list(request)
        # Add custom stats
        stats = self.get_stats()
        app_list.append({
            'name': 'Analytics',
            'app_label': 'analytics',
            'models': [{
                'name': 'Statistics',
                'object_name': 'Statistics',
                'admin_url': '#',
                'view_only': True,
                'stats': stats
            }]
        })
        return app_list
    
    def get_stats(self):
        # Cache the stats for 1 hour
        stats = cache.get('admin_dashboard_stats')
        if stats is not None:
            return stats
            
        now = timezone.now()
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)
        
        # Contact messages stats
        total_messages = ContactMessage.objects.count()
        unread_messages = ContactMessage.objects.filter(is_read=False).count()
        recent_messages = ContactMessage.objects.filter(created_at__gte=last_week).count()
        
        # Services stats
        total_services = Service.objects.count()
        active_services = Service.objects.filter(is_active=True).count()
        
        # Blog stats
        total_posts = Post.objects.count()
        published_posts = Post.objects.filter(published=True).count()
        recent_posts = Post.objects.filter(created_at__gte=last_month).count()
        
        stats = {
            'messages': {
                'total': total_messages,
                'unread': unread_messages,
                'recent': recent_messages,
            },
            'services': {
                'total': total_services,
                'active': active_services,
            },
            'posts': {
                'total': total_posts,
                'published': published_posts,
                'recent': recent_posts,
            }
        }
        
        cache.set('admin_dashboard_stats', stats, 3600)  # Cache for 1 hour
        return stats
