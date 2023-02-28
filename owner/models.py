from django.db import models
from django.contrib.auth.models import User

# DropDown List items for gender field
CAR_CHOICES = (
    ("suv", "SUV"),
    ("hatchback", "Hatchback"),
    ("crossover", "Crossover"),
    ("convertible", "Convertible"),
    ("sedan", "Sedan"),
    ("sports", "Sports"),
    ("coupe", "Coupe"),
    ("minivan", "Minivan"),
    ("station wagon", "Station Wagon"),
    ("pickup truck", "Pickup Truck"),
)


class AddProduct(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.ForeignKey(User, null=False, on_delete=models.CASCADE, blank=False)
    car_type = models.CharField(max_length=100, choices=CAR_CHOICES)
    owner_name = models.CharField(max_length=120)
    company_name = models.CharField(max_length=150)
    model_name = models.CharField(max_length=150)
    car_image = models.ImageField(blank=True,upload_to="media/")
    car_number = models.CharField(max_length=15, unique=True)
    passing_year = models.IntegerField()
    per_day_rent = models.IntegerField()
    is_available = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Product Details"
        verbose_name_plural = "Add Product"

    def __str__(self):
        return self.email.username
