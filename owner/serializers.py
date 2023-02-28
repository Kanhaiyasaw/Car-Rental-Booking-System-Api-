from rest_framework import serializers
from owner.models import AddProduct
from authentication.models import CustomerDetail


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddProduct
        fields = [
            "car_type",
            "owner_name",
            "company_name",
            "model_name",
            "car_number",
            "passing_year",
            "per_day_rent"
        ]

    def create(self, validated_data):
        return AddProduct.objects.create(
            email=self.context.get("user"), **validated_data
        )
    def update(self, instance, validated_data):
        instance.car_type = validated_data["car_type"]
        instance.owner_name = validated_data["owner_name"]
        instance.company_name = validated_data["company_name"]
        instance.model_name = validated_data["model_name"]
        instance.car_number = validated_data["car_number"]
        instance.passing_year = validated_data["passing_year"]
        instance.per_day_rent = validated_data["per_day_rent"]

        instance.save()
        return super().update(instance=instance, validated_data=validated_data)


class ReceivedConfirmationSerializer(serializers.Serializer):
    car_number = serializers.CharField(required=True)
    customer_email = serializers.EmailField(required=True)
    pickup_date = serializers.DateField(required=True)
    book_status = serializers.BooleanField(required=True)

    def validate(self, attrs):
        car_number = attrs.get("car_number")
        email = attrs.get("customer_email")
        customer = CustomerDetail.objects.filter(user__email=email).exists()
        product = AddProduct.objects.filter(car_number=car_number, is_available=True).exists()
        if customer is False:
            raise serializers.ValidationError("That Customer not Valid")
        if product is False:
            raise serializers.ValidationError("That product is not exists")
        return attrs
