from django.db import models

from shop.models import ProductVariant, Flavour
from django.contrib.auth.models import User
from user.models import CustomUser


# # Create your models here.
class CartItem(models.Model):
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.variant.product.name} - quantity: {self.quantity} id: {self.variant.id}"
