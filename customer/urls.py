from django.urls import path
from customer.views import CustomerSideCarView

# urls
urlpatterns = [
    path("search/", CustomerSideCarView.as_view(), name="search_car"),
    path("order/", CustomerSideCarView.as_view(), name="order"),
    
]
