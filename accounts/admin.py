from django.contrib import admin
from .models import Member, OTP

# Register your models here.
@admin.register(Member)
class MemberAdminModel(admin.ModelAdmin):
    list_display = ("phone", "gender", "address" ,"date_joined")
    search_fields = ("phone", "address")
    list_filter = ("date_joined",)

@admin.register(OTP)
class OTPAdminModel(admin.ModelAdmin):
    list_display = ("created_at", "expires_at" ,"attempts", "is_used")
    search_fields = ("created_at", "expires_at")
    list_filter = ("created_at",)