from rest_framework import serializers
from django.contrib.auth.models import User


class UserChangePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        max_length=255, required=True, style={"input_type": "password", "write_only": True}
    )
    password2 = serializers.CharField(
        max_length=255, required=True, style={"input_type": "password", "write_only": True}
    )

    class Meta:
        fields = ["password", "password2"]

    def validate(self, attrs):
        # Checks password and comfirm password input
        password = attrs.get("password")
        password2 = attrs.get("password2")

        user = self.context.get("user")  # Creating user object
        if password != password2:
            raise serializers.ValidationError(
                {"status": False, "msg": "Password Doesnt Match"}
            )
        user.set_password(password)
        user.save()
        return attrs
