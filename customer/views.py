from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from customer.serializers import SendOrderSerializer
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from owner.models import AddProduct
from helper.order import send_order_email
from authentication.models import CustomerDetail
from django.db.models import Q
from django.contrib.auth.models import User


class CustomerSideCarView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        group = request.user.groups.get().name
        if group != settings.GRP_CUSTOMER:
            response = {
                "status": False,
                "message": "Customer Only Can See",
                "data": None,
            }
            return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        model = request.query_params.get("by_model")
        company = request.query_params.get("by_company")
        rent = request.query_params.get("by_rent")
        type = request.query_params.get("by_type")
        pass_year = request.query_params.get("by_passing_year")

        if len(request.query_params) == 0:

            car_obj = AddProduct.objects.filter(is_available=True).values(
                "car_type",
                "company_name",
                "model_name",
                "car_number",
                "passing_year",
                "per_day_rent",
            )
        else:
            car_obj = AddProduct.objects.filter(
                Q(is_available=True)
                & (
                    Q(car_type=type)
                    | Q(company_name=company)
                    | Q(model_name=model)
                    | Q(passing_year=pass_year)
                    | Q(per_day_rent=rent)
                )
            ).values(
                "car_type",
                "company_name",
                "model_name",
                "car_number",
                "passing_year",
                "per_day_rent",
            )
        response = {"status": True, "message": "Car Details", "data": car_obj}
        return Response(data=response, status=status.HTTP_200_OK)

    # send Order notification to the car owner
    def post(self, request, format=None):
        serializer = SendOrderSerializer(data=request.data)
        if serializer.is_valid():
            usr_obj = AddProduct.objects.filter(car_number=request.data["car_number"])
            
            if usr_obj:
                owner_email = usr_obj.values("email__email")[0]["email__email"]
                customer_obj = CustomerDetail.objects.get(user=request.user)
                product_obj = AddProduct.objects.get(
                    car_number=request.data["car_number"]
                )
                # send mail to the car owner for order notification
                send_order_email(
                    owner_email,
                    product_obj,
                    customer_obj,
                )
                return Response(
                    {
                        # Success response
                        "status": True,
                        "message": "Order sent to the Owner. Wait for confirmation mail",
                        "data": None,
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                # faild response
                response = {
                    "status": False,
                    "message": "Product not Exists",
                    "data": None,
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        # failed response
        response = {"status": False, "message": serializer.errors, "data": None}
        return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
