from django.contrib import admin
from .models import Book
from notifications.utils import notify_admin

# Register your models here.
@admin.register(Book)
class BookAdminModel(admin.ModelAdmin):
    list_display = ("title", "author", "isbn", "category", "publisher", "year", "price", "quantity")
    search_fields = ("title", "author", "category", "price")
    list_filter = ("title",)

    def save_model(self, request, obj, form, change):
        old_quantity = None
        if change:
            old_quantity = Book.objects.get(pk=obj.pk).quantity
        super().save_model(request, obj, form, change)
        if old_quantity is not None:
            if old_quantity > 0 and obj.quantity == 0:
                notify_admin(f"{obj.title} is now out of stock.")