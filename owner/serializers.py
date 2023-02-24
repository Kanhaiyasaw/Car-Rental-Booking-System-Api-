from rest_framework import serializers
from owner.models import AddProduct
from authentication.models import CustomerDetail


class AddProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddProduct
        fields = [
            "car_type",
            "owner_name",
            "company_name",
            "model_name",
            "car_number",
            "passing_year",
            "per_day_rent",
        ]

    def create(self, validated_data):
        return AddProduct.objects.create(
            email=self.context.get("user"), **validated_data
        )


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
