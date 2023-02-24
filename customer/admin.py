from django.contrib import admin
from customer.models import BoookedCarDetail

@admin.register(BoookedCarDetail)
class CustomerProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "car_id",
        "car_type",
        "owner_name",
        "company_name",
        "model_name",
        "car_number",
        "date_of_pickup",
        "per_day_rent",
        "is_active"
    )