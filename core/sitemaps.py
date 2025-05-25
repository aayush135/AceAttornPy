from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from blog.models import Post

class StaticViewSitemap(Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['core:home', 'core:about', 'core:services', 'core:contact']

    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.6

    def items(self):
        return Post.objects.filter(published=True)

    def lastmod(self, obj):
        return obj.updated_at
