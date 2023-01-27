from rest_framework import serializers

from owner.models import AddProduct


class SendOrderSerializer(serializers.Serializer):
    product_id = serializers.IntegerField(required=True)
