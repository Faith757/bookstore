from django.contrib import admin
from .models import bookRequest
from notifications.utils import notify_member

# Register your models here.
@admin.register(bookRequest)
class bookRequestAdminModel(admin.ModelAdmin):
    list_display = ("title", "category", "date_requested", "status")
    search_fields = ("title", "category", 'status')
    list_filter = ("title",)

    def save_model(self, request, obj, form, change):
        old_status = None
        if change:
            old_status = bookRequest.objects.get(pk=obj.pk).status
            super().save_model(request, obj, form, change)

        if old_status == 'pending' and obj.status == 'approved':
            notify_member(
                obj.member,
                f'Your requested book, {obj.title}, is now available.'
            )
        
        if old_status == 'pending' and obj.status == 'rejected':
            notify_member(
                obj.member,
                f'Your book request for {obj.title} has been rejected.'
            )
        
        if old_status == 'rejected' and obj.status == 'approved':
            notify_member(
                obj.member,
                f'Your book request for {obj.title} has been approved.'
            )