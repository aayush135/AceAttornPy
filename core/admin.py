from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.db.models import Count
from django.utils import timezone
from datetime import timedelta
from .models import Service, ContactMessage

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'order', 'created_at', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'short_description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ('order',)
    list_editable = ('is_active', 'order')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'icon', 'order', 'is_active')
        }),
        ('Content', {
            'fields': ('short_description', 'description')
        }),
    )

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read', 'sent_successfully', 'message_preview')
    list_filter = ('is_read', 'sent_successfully', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('created_at', 'sent_successfully')
    ordering = ('-created_at',)
    list_editable = ('is_read',)
    
    def message_preview(self, obj):
        return obj.message[:100] + '...' if len(obj.message) > 100 else obj.message
    message_preview.short_description = 'Message Preview'

    def changelist_view(self, request, extra_context=None):
        # Get statistics for the dashboard
        stats = self.get_dashboard_stats()
        extra_context = extra_context or {}
        extra_context.update(stats)
        return super().changelist_view(request, extra_context=extra_context)

    def get_dashboard_stats(self):
        now = timezone.now()
        last_week = now - timedelta(days=7)
        last_month = now - timedelta(days=30)

        stats = {
            'total_messages': ContactMessage.objects.count(),
            'unread_messages': ContactMessage.objects.filter(is_read=False).count(),
            'recent_messages': ContactMessage.objects.filter(created_at__gte=last_week).count(),
            'total_services': Service.objects.count(),
            'active_services': Service.objects.filter(is_active=True).count(),
        }
        return stats

    class Media:
        css = {
            'all': ('admin/css/dashboard.css',)
        }
        js = ('admin/js/dashboard.js',)

# Customize admin site
admin.site.site_header = 'AceAttorn Legal Solutions Admin'
admin.site.site_title = 'AceAttorn Admin Portal'
admin.site.index_title = 'Welcome to AceAttorn Admin Portal'
