from django.urls import path
from dashboard import views

urlpatterns = [
    path("edit_profile/", views.update_profile, name="edit_profile"),
    path("change_password/", views.change_pass, name="change_password"),
]
