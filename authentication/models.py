from django.db import models
from django.contrib.auth.models import User

# That Store Owner detail and Extra detail
class OwnerDetail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, blank=False)
    phone = models.BigIntegerField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Owner Details"
        verbose_name_plural = "Owner Details"
    
    def __str__(self):
        return str(self.user)

# this Store Customer Detail And extra detail
class CustomerDetail(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, blank=False)
    phone = models.BigIntegerField()
    address = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "customer Details"
        verbose_name_plural = "customer Details"
