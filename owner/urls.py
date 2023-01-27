from django.urls import path
from owner.views import AddProductView, OwnerOprations

urlpatterns = [
    path('profile/', OwnerOprations.as_view(), name="profile"),

    path("addproduct/", AddProductView.as_view(), name="add_product"),
    path("list/", AddProductView.as_view(), name="car_list"),
]
