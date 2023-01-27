from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from owner.serializers import AddProductSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from owner.models import AddProduct
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
            "data":{
                "email":str(user),
                "first name":owner_obj.user.first_name,
                "last_name":owner_obj.user.last_name,
                "phone number":owner_obj.phone,
                "address":owner_obj.address
                }
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
        serializer = AddProductSerializer(data = request.data, context={"user": request.user})
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