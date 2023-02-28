from rest_framework.views import APIView
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from owner.serializers import ProductSerializer, ReceivedConfirmationSerializer
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


class ProductView(APIView):
    permission_classes = [IsAuthenticated]

    # <-------------Add New Car------------------>
    def post(self, request, format=None):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": settings.ONLY_OWNER_LOGIN,
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        try:
            with transaction.atomic():
                serializer = ProductSerializer(
                    data=request.data, context={"user": request.user}
                )
                if serializer.is_valid():
                    obj = serializer.save()

                    # return Success Response
                    response = {
                        "status": True,
                        "message": "New Car Registered successfully",
                        "data": obj.id,
                    }
                    return Response(data=response, status=status.HTTP_201_CREATED)

                response = {"status": False, "message": serializer.errors, "data": None}
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            response = {
                "status": False,
                "message": "Something Went Wrong",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

    # <-------------Get Car detail--------------->
    def get(self, request, format=None):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": settings.ONLY_OWNER_LOGIN,
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        user = request.user

        car_obj = AddProduct.objects.filter(email=user).values()

        response = {"status": True, "message": "Car Details", "data": car_obj}
        return Response(data=response, status=status.HTTP_200_OK)

    # <-------------Update Car Detail------------>
    def put(self, request):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": settings.ONLY_OWNER_LOGIN,
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        id = request.query_params.get("id")
        user = request.user
        if AddProduct.objects.filter(pk=id, email=user, is_available=True):

            car_obj = AddProduct.objects.get(pk=id)

            serializer = ProductSerializer(car_obj, data=request.data)

            if serializer.is_valid():

                serializer.save()

                # success response
                response = {
                    "status": True,
                    "message": "Update Successfully",
                    "data": None,
                }
                return Response(data=response, status=status.HTTP_200_OK)

            # If serialize error occur
            response = {"status": False, "message": serializer.errors, "data": None}
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # If car is not available in system
        response = {"status": False, "message": "data not found", "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        # record not exists
        response = {"status": False, "message": "Data Not Found", "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    # <-------------Update Car image------------->
    def patch(self, request):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": settings.ONLY_OWNER_LOGIN,
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        id = request.query_params.get("id")
        user = request.user
        if AddProduct.objects.filter(pk=id, email=user, is_available=True):

            car_obj = AddProduct.objects.get(pk=id)

            # if car available
            car_obj.car_image = request.data["car_pic"]
            car_obj.save()

            # Success Response
            response = {"status": True, "massage": "car image update", "data": None}
            return Response(data=response, status=status.HTTP_200_OK)

            # Data Not Found
        response = {"status": False, "massage": "data not Found", "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

    # <-------------delete Car details------------->
    def delete(self, request):
        group = request.user.groups.get().name
        if group != settings.GRP_OWNER:
            response = {
                "status": False,
                "message": settings.ONLY_OWNER_LOGIN,
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        id = request.query_params.get("id")
        user = request.user
        if AddProduct.objects.filter(pk=id, email=user, is_available=True):

            car_obj = AddProduct.objects.get(pk=id)

            # if car available
            car_obj.delete()
            car_obj.save()

            # Success Response
            response = {"status": True, "massage": "Car Deleted Succefully", "data": None}
            return Response(data=response, status=status.HTTP_200_OK)

            # Data Not Found
        response = {"status": False, "massage": "data not Found", "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
    

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

            product_obj = AddProduct.objects.get(
                car_number=request.data["car_number"], is_available=True
            )
            customer_email = request.data["customer_email"]
            booking_status = request.data["book_status"]
            if booking_status == "True":
                confirmation_mail(customer_email, product_obj)

                product_obj.is_available = False
                product_obj.save()

                booking_car_obj = {
                    "car_type": product_obj.car_type,
                    "owner_name": product_obj.owner_name,
                    "company_name": product_obj.company_name,
                    "model_name": product_obj.model_name,
                    "car_number": product_obj.car_number,
                    "date_of_pickup": request.data["pickup_date"],
                    "is_active": True,
                    "per_day_rent": product_obj.per_day_rent,
                }

                book_obj = BoookedCarDetail.objects.create(
                    car_id=product_obj, **booking_car_obj
                )

                book_obj.save()
                response = {
                    "status": True,
                    "message": "Car Booking Mail is sent to the Customer. Thank you!",
                    "data": None,
                }
                return Response(data=response, status=status.HTTP_200_OK)
            else:
                decline_order_mail(customer_email, product_obj)
                response = {
                    "status": True,
                    "message": "Custemer Decline Request Mail is sent. Thank you!",
                    "data": None,
                }
                return Response(data=response, status=status.HTTP_200_OK)
        response = {"status": False, "message": serializer.errors, "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
