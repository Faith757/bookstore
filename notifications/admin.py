from django.contrib import admin
from .models import Notification

# Register your models here.
@admin.register(Notification)
class NotificationAmin(admin.ModelAdmin):
    list_display = ('recipient', 'notification_type', 'message', 'is_read', 'date_created')
    search_fields = ('notification_type', 'message')
    filter_list = ('is_read',)