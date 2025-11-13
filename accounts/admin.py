from django.contrib import admin
from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone_number', 'city', 'state', 'is_verified', 'created_at']
    list_filter = ['city', 'state', 'is_verified', 'created_at']
    search_fields = ['user__username', 'user__email', 'phone_number']
    readonly_fields = ['created_at', 'updated_at']
    list_editable = ['is_verified']
