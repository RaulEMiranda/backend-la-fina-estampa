from django.db import models
from .CustomerModel import Customer
from .CouponModel import Coupon


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders")
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    coupon = models.ForeignKey(
        Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField(max_length=20, choices=[(
        "pending", "Pendiente"), ("paid", "Pagado"), ("shipped", "Enviado")], default="pending")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden {self.id} - {self.customer.user.username}"
