from django.urls import path
from userprofile.views import UserProfileView


urlpatterns = [
    path("profile/", UserProfileView.as_view(), name="profile"),
    path("change-password/", UserProfileView.as_view(), name="change-password"),
    path("update/", UserProfileView.as_view(), name="change-password"),
    path("delete/", UserProfileView.as_view(), name="delete"),
]
