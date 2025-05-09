from django.db import models
from apps.products.models import Product


class Inventory(models.Model):
    product   = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity  = models.PositiveIntegerField()
    is_active = models.BooleanField(default=True)  # logical delete

    def __str__(self):
        return f"{self.product.name} – {self.quantity}"