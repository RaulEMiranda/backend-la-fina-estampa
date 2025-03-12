from django.db import models

class Coupon(models.Model):
    code = models.CharField(max_length=20, unique=True)  # Código del cupón (Ej: DESCUENTO5)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2)  # Ej: 5.00 = S/5 de descuento
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.code
