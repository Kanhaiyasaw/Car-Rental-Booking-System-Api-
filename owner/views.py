from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from owner.serializers import AddProductSerializer, ReceivedConfirmationSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from owner.models import AddProduct
from helper.order import confirmation_mail, decline_order_mail
from customer.models import BoookedCarDetail
from authentication.models import CustomerDetail
from django.contrib.auth.models import User
from authentication.models import OwnerDetail


class OwnerOprations(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": "Child Only Can add See",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        owner_obj = OwnerDetail.objects.get(user=user)
        response = {
            "status": True,
            "message": "Profile of User",
            "data": {
                "email": str(user),
                "first name": owner_obj.user.first_name,
                "last_name": owner_obj.user.last_name,
                "phone number": owner_obj.phone,
                "address": owner_obj.address,
            },
        }
        return Response(data=response, status=status.HTTP_200_OK)


class AddProductView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": "Owner Only Can add Car",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        serializer = AddProductSerializer(
            data=request.data, context={"user": request.user}
        )
        if serializer.is_valid():
            serializer.save()

            # return Success Response
            response = {
                "status": True,
                "message": "New Car Registered successfully",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)
        response = {"status": False, "message": serializer.errors, "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, format=None):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": "Child Only Can add See",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        user = request.user
        car_obj = AddProduct.objects.filter(email=user).values()
        response = {"status": True, "message": "Car Details", "data": car_obj}
        return Response(data=response, status=status.HTTP_200_OK)


class ConfirmationMailView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": "Owner Only Can give confermation to the customer",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        serializer = ReceivedConfirmationSerializer(data=request.data)

        if serializer.is_valid():

            product_obj = AddProduct.objects.get(car_number=request.data["car_number"])
            customer_email = request.data["customer_email"]
            booking_status = request.data["book_status"]
            if booking_status == "True":
                confirmation_mail(customer_email, product_obj)

                product_obj.is_available = False
                product_obj.save()

                booking_car_obj = {
                    "car_type":product_obj.car_type,
                    "owner_name":product_obj.owner_name,
                    "company_name":product_obj.company_name,
                    "model_name":product_obj.model_name,
                    "car_number":product_obj.car_number,
                    "date_of_pickup":request.data["pickup_date"],
                    "is_active":True,
                    "per_day_rent":product_obj.per_day_rent
                }

                book_obj = BoookedCarDetail.objects.create(car_id=product_obj, **booking_car_obj)

                book_obj.save()
                response = {
                    "status":True,
                    "message":"Car Booking Mail is sent to the Customer. Thank you!",
                    "data":None
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                decline_order_mail(customer_email, product_obj)
                response = {
                    "status":True,
                    "message":"Custemer Decline Request Mail is sent. Thank you!",
                    "data":None
                }
                return Response(data=response, status=status.HTTP_200_OK)
        response = {
                "status":False,
                "message":serializer.errors,
                "data":None
                }
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)