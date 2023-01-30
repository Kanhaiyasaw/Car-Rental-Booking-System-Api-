from rest_framework import serializers

from owner.models import AddProduct


class SendOrderSerializer(serializers.Serializer):
    car_number = serializers.CharField(required=True)
