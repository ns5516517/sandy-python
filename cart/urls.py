from django.urls import path
from cart import views

app_name = "cart"

urlpatterns = [
    path("cart/", views.view_cart, name="view_cart"),
    path("add/<int:variant_id>", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:variant_id>", views.remove_from_cart, name="remove_from_cart"),
    path("update-cart/", views.update_to_cart, name="update_from_cart"),
]
