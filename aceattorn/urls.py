from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from core.sitemaps import StaticViewSitemap, BlogSitemap
from django.views.generic import TemplateView
from django.http import HttpResponse

# Register the default admin site
admin.site.site_header = 'AceAttorn Legal Solutions Admin'
admin.site.site_title = 'AceAttorn Admin Portal'
admin.site.index_title = 'Welcome to AceAttorn Admin Portal'

sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('analytics/', include('analytics.urls')),
    path('', include('django_prometheus.urls')),  # Prometheus metrics
    path('oauth2callback/', lambda request: HttpResponse('Authorization successful! You can close this window.')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('robots.txt', TemplateView.as_view(template_name="robots.txt", content_type="text/plain")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
