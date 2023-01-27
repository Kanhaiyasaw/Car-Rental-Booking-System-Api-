from rest_framework import serializers
from owner.models import AddProduct


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddProduct
        fields = [
            "car_type",
            "owner_name",
            "company_name",
            "model_name",
            "passing_year",
            "per_day_rent"
        ]

    def create(self, validated_data):
        return AddProduct.objects.create(email=self.context.get("user"), **validated_data)
