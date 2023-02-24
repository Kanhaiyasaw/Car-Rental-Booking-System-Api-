from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from authentication.serializers import (
    OwnerRegistrationSerializer,
    CustomerRegistrationSerializer,
)


class CustomerRegistrationView(APIView):
    # Class bases view for user registration
    def post(self, request, format=None):
        # Passing our data in the seriealizer
        serializer = CustomerRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Throws error if data is empty or not correct
            return Response(
                {
                    "status": True,
                    "message": "Customer Registered Successfully",
                    "data": None,
                },
                status=status.HTTP_201_CREATED,
            )

        # All serializer error stores in errors
        response = {"status": False, "errors": serializer.errors, "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


class OwnerRegestrationView(APIView):
    def post(self, request, format=None):
        # Passing our data in the seriealizer
        serializer = OwnerRegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()  # Throws error if data is empty or not correct
            return Response(
                {
                    "status": True,
                    "message": "Car Owner Registered Successfully",
                    "data": None,
                },
                status=status.HTTP_201_CREATED,
            )

        # All serializer error stores in errors
        response = {"status": False, "errors": serializer.errors, "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)


# Login User
class UserLoginView(APIView):
    # Class bases view for user Login
    def post(self, request, format=None):
        if "email" in request.data:
            email = request.data["email"]
        else:
            # if email is not given in response body
            return Response(
                {
                    "status": False,
                    "message": {"email": ["This field is required."]},
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if "password" in request.data:
            password = request.data["password"]
        else:
            # if password is not give in response body
            return Response(
                {
                    "status": False,
                    "errors": {"password": ["This field is required."]},
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if not User.objects.filter(email=email).exists():
            return Response(
                {
                    "status": False,
                    "message": "No User exist with this email",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        user_obj = User.objects.get(email=email)
        if user_obj.is_active:  # Only lets login is user status is active
            # Passing our data in the seriealizer

            username = User.objects.get(email=email).username
            user = authenticate(username=username, password=password)
            Token.objects.filter(user=user).delete()
            if user is not None:
                # Genrate Token if given username and password verify
                token, _ = Token.objects.get_or_create(user=user)
                return Response(
                    {
                        "status": True,
                        "message": "Authentication Successful",
                        "data": {"token": token.key},
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # Return error is invalid username or password given
                return Response(
                    {
                        "status": False,
                        "errors": "Invalid Email or Password",
                        "data": None,
                    },
                    status=status.HTTP_404_NOT_FOUND,
                )
        else:
            # Returns error response if user is_active = False
            return Response(
                {
                    "status": False,
                    "errors": "User Currently Disabled. Please Try again",
                    "data": None,
                },
                status=status.HTTP_404_NOT_FOUND,
            )


