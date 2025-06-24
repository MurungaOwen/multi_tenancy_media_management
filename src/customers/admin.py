from django.contrib import admin
from django_tenants.utils import get_public_schema_name, get_tenant_model
from django.db import connection
from .models import Client, Domain
from django_tenants.admin import TenantAdminMixin


# Register your models here.
if connection.schema_name == get_public_schema_name():
    print("our schema is {} - public schema".format(connection.schema_name))
    @admin.register(Client)
    class ClientAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name', 'paid_until')

    admin.site.register(Domain)