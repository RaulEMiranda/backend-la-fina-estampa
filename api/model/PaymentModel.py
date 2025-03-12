from django.db import models
from.OrderModel import Order


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=50, choices=[("card", "Tarjeta"), ("paypal", "PayPal"), ("bank", "Transferencia Bancaria")])
    transaction_id = models.CharField(max_length=255, unique=True)
    paid_at = models.DateTimeField(auto_now_add=True)
