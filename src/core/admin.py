from django.contrib import admin
from .models import TenantKey
from .utils import rotate_tenant_key_and_reencrypt


# Register your models here.
@admin.register(TenantKey)
class TenantKeyAdmin(admin.ModelAdmin):
    list_display = ['name']
    readonly_fields = ['fernet_key']
    actions = ['rotate_and_reencrypt']

    def rotate_and_reencrypt(self, request, queryset):
        if queryset.count() != 1:
            self.message_user(request, "Select exactly one key to rotate.")
            return
        updated = rotate_tenant_key_and_reencrypt()
        self.message_user(request, f"Key rotated. {len(updated)} documents updated.")

    rotate_and_reencrypt.short_description = "\u21bb Rotate Fernet Key + Re-encrypt All Docs"

