# Generated by Django 4.1.5 on 2023-01-27 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('owner', '0006_addproduct_car_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='addproduct',
            name='car_number',
            field=models.CharField(max_length=15, unique=True),
        ),
    ]
