from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator
from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from authentication.models import OwnerDetail, CustomerDetail

# serilizer for extra field of Owner
class OwnerExtraDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerDetail
        fields = ["phone", "address"]


# Owner Registration
class OwnerRegistrationSerializer(serializers.ModelSerializer):
    # Registration Serializer
    extra_details = OwnerExtraDetailsSerializer()
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=("email already exists"),
            )
        ],
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "extra_details"]
        extra_kwarg = {"password": {"write_only": True}}

    def create(self, validate_data):
        # Creation/registration of the user as Doctor
        group = Group.objects.get(name=settings.GRP_OWNER)

        user_details = {
            "username": validate_data["email"],
            "email": validate_data["email"],
            "first_name": validate_data["first_name"],
            "last_name": validate_data["last_name"],
            "password": make_password(validate_data["password"]),
        }
        user = User.objects.create(**user_details)
        user.groups.add(group)
        user.save()

        extra_detail = {
            "phone": validate_data["extra_details"]["phone"],
            "address": validate_data["extra_details"]["address"],
        }
        return OwnerDetail.objects.create(user=user, **extra_detail)


# serilizer for extra field of Customer
class CustomerExtraDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OwnerDetail
        fields = ["phone", "address"]

# Customer Registration 
class CustomerRegistrationSerializer(serializers.ModelSerializer):
    # Registration Serializer
    extra_details = CustomerExtraDetailsSerializer()
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(
        required=True,
        validators=[
            UniqueValidator(
                queryset=User.objects.all(),
                message=("email already exists"),
            )
        ],
    )

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "extra_details"]
        extra_kwarg = {"password": {"write_only": True}}

    def create(self, validate_data):
        # Creation/registration of the user as Doctor
        group = Group.objects.get(name=settings.GRP_CUSTOMER)

        user_details = {
            "username": validate_data["email"],
            "email": validate_data["email"],
            "first_name": validate_data["first_name"],
            "last_name": validate_data["last_name"],
            "password": make_password(validate_data["password"]),
        }
        user = User.objects.create(**user_details)
        user.groups.add(group)
        user.save()

        extra_detail = {
            "phone": validate_data["extra_details"]["phone"],
            "address": validate_data["extra_details"]["address"],
        }
        return CustomerDetail.objects.create(user=user, **extra_detail)
