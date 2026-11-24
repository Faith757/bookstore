from django.contrib import admin
from .models import Order, orderItem

# Register your models here.
@admin.register(Order)
class OrderAdminModel(admin.ModelAdmin):
    list_display = ("payment_reference", "date_ordered", "total_amount", "payment_receipt", "status", "payment")
    search_fields = ("date_ordered", "status", "payment", "total_amount")
    list_filter = ("payment_reference",)

@admin.register(orderItem)
class orderItemAdminModel(admin.ModelAdmin):
    list_display = ("book_title", "price", "quantity")
    search_fields = ("book_title", "price")
    list_filter = ("book_title",)