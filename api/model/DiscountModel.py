from django.db import models
from .ProductModel import Product


class Discount(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="discount")
    discount_percentage = models.DecimalField(
        max_digits=5, decimal_places=2)  # Ej: 10.00 = 10% de descuento
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
