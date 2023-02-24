from django.db import models
from owner.models import AddProduct

# that moodel store the data which car is successfully booked by the specific customer
class BoookedCarDetail(models.Model):
    id = models.AutoField(primary_key=True)
    car_id = models.ForeignKey(
        AddProduct, null=False, on_delete=models.DO_NOTHING, blank=False
    )
    car_type = models.CharField(max_length=100)
    owner_name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=150)
    model_name = models.CharField(max_length=150)
    car_number = models.CharField(max_length=15)
    date_of_pickup = models.DateField()
    is_active = models.BooleanField()
    per_day_rent = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Booked Car "
        verbose_name_plural = "Booked Car"
