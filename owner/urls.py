from django.urls import path
from owner.views import ProductView, OwnerOprations, ConfirmationMailView

urlpatterns = [
    path("profile/", OwnerOprations.as_view(), name="profile"),
    path("addproduct/", ProductView.as_view(), name="add_product"),
    path("update_car/", ProductView.as_view(), name="update_car"),
    path("update_car_pic/", ProductView.as_view(), name="update_car_pic"),
    path("list/", ProductView.as_view(), name="car_list"),
    path(
        "order_confirmation_mail/", ConfirmationMailView.as_view(), name="order_confirm"
    ),
]
