from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from authentication.models import OwnerDetail, CustomerDetail
from django.contrib.auth.models import Group
from django.conf import settings
from django.contrib.auth.models import User
from userprofile.serializers import UserChangePasswordSerializer


class UserProfileView(APIView):
    # Class bases to view user profile after successful login
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = request.user
        group = str(request.user.groups.get())
        if group == "Owner":
            extra_details_obj = OwnerDetail.objects.get(user=user)

            email = str(user.email)

            # Sending all details of the doctor
            data = {
                "status": True,
                "message": "Login Success",
                "data": {
                    "id": user.id,
                    "email": email,
                    "type": group,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": extra_details_obj.phone,
                    "address": extra_details_obj.address,
                },
            }
            # Returns the above values only when user login token is valid
            return Response(data, status=status.HTTP_200_OK)
        else:
            extra_details_obj = CustomerDetail.objects.get(user=user)

            email = str(user.email)

            # Sending all details of the doctor
            data = {
                "status": True,
                "message": "Login Success",
                "data": {
                    "id": user.id,
                    "email": email,
                    "username": email.split("@")[0],
                    "type": group,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "phone": extra_details_obj.phone,
                    "address": extra_details_obj.address,
                },
            }
            # Returns the above values only when user login token is valid
            return Response(data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        # Post method to update password
        serializer = UserChangePasswordSerializer(
            data=request.data, context={"user": request.user}
        )

        if serializer.is_valid():
            return Response(
                {
                    "status": True,
                    "message": "Password Changed Successful",
                    "data": None,
                },
                status=status.HTTP_200_OK,
            )

        # If password doesn't match
        return Response(
            {"status": False, "message": "Password Doesnt Match", "data": None},
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, *args, **kwargs):
        # Partial update for first_name and last_name
        user = request.user
        data = request.data

        if len(data) == 0:
            # If blank body sent in responce
            return Response(
                {
                    "status": False,
                    "message": "Either enter first_name or last_name",
                    "data": None,
                }
            )

        user.first_name = data.get("first_name", user.first_name)
        user.last_name = data.get("last_name", user.last_name)

        user.save()

        return Response(
            {"status": True, "message": "Data Updated Successful", "data": None},
            status=status.HTTP_200_OK,
        )

    def delete(self, request, format=None):
        # Soft deleting | Turning is_active to False on delete
        user = request.user
        user.is_active = False
        user.save()
        return Response(
            {"status": True, "message": "User Deleted Successful", "data": None},
            status=status.HTTP_200_OK,
        )
    