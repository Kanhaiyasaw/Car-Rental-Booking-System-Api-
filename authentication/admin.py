from django.contrib import admin
from authentication.models import CustomerDetail, OwnerDetail


@admin.register(OwnerDetail)
class OwnermodelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "address")


@admin.register(CustomerDetail)
class CustomermodelAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "phone", "address")
