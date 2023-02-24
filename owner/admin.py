from django.contrib import admin
from owner.models import AddProduct


@admin.register(AddProduct)
class OwnerProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "email",
        "car_type",
        "owner_name",
        "company_name",
        "car_number",
        "model_name",
        "passing_year",
        "per_day_rent",
        "is_available"
    )
