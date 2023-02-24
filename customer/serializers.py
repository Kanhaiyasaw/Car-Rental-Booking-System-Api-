from rest_framework import serializers

from owner.models import AddProduct

# serializer for validation of car number 
class SendOrderSerializer(serializers.Serializer):
    car_number = serializers.CharField(required=True)
