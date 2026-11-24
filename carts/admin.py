from django.contrib import admin
from .models import Cart

# Register your models here.
@admin.register(Cart)
class CartAdminModel(admin.ModelAdmin):
    list_display = ("book", "quantity", "date_added", "stock_reserved")
    search_fields = ("book", "date_added")
    list_filter = ("date_added",)