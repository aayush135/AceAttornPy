from django.utils import timezone
from .models import PageView, UserEngagement
import redis
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        try:
            self.redis = redis.Redis(
                host=settings.REDIS_HOST,
                port=settings.REDIS_PORT,
                db=0,
                socket_timeout=2
            )
            self.redis.ping()  # Test connection
        except Exception as e:
            logger.error(f"Redis connection failed: {e}")
            self.redis = None

    def __call__(self, request):
        # Process request
        start_time = timezone.now()
        
        response = self.get_response(request)
        
        try:
            # Skip static files and admin
            if not any(path in request.path for path in ['/static/', '/media/', '/admin/', '/favicon.ico']):
                # Ensure session key exists
                if not request.session.session_key:
                    request.session.create()
                
                # Record page view
                page_view = PageView.objects.create(
                    path=request.path,
                    ip_address=self.get_client_ip(request),
                    user_agent=request.META.get('HTTP_USER_AGENT', ''),
                    user=request.user if request.user.is_authenticated else None,
                    session_key=request.session.session_key,
                    referrer=request.META.get('HTTP_REFERER', '')
                )
                
                # Update real-time stats in Redis
                if self.redis:
                    try:
                        self.redis.incr('current_page_views')
                        self.redis.expire('current_page_views', 300)  # Expire after 5 minutes
                        
                        if request.user.is_authenticated:
                            self.redis.sadd('active_users', request.user.id)
                            self.redis.expire('active_users', 300)
                            
                        # Store session activity
                        session_key = f"session:{request.session.session_key}"
                        self.redis.hincrby(session_key, 'page_views', 1)
                        self.redis.expire(session_key, 1800)  # 30 minutes
                        
                    except redis.RedisError as e:
                        logger.error(f"Redis operation failed: {e}")
                
                # Create basic engagement record
                UserEngagement.objects.create(
                    user=request.user if request.user.is_authenticated else None,
                    session_key=request.session.session_key,
                    page_time=0,  # Will be updated via JavaScript
                    scroll_depth=0,  # Will be updated via JavaScript
                    path=request.path
                )
                
        except Exception as e:
            logger.error(f"Analytics tracking failed: {e}")
        
        return response
    
    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR', '')
        return ip
