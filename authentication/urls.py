from django.urls import path
from authentication.views import (
    OwnerRegestrationView,
    CustomerRegistrationView,
    UserLoginView,
)
# urls 
urlpatterns = [
    path("owner_register/", OwnerRegestrationView.as_view(), name="owner_register"),
    path(
        "customer_register/",
        CustomerRegistrationView.as_view(),
        name="customer_register",
    ),
    path("login/", UserLoginView.as_view(), name="login"),
]
