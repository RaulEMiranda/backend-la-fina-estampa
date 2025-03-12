from django.db import models
from .CategoryModel import Category
from .SubcategoryModel import Subcategory
import cloudinary.models
from django.utils.timezone import now

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products')
    subcategory = models.ForeignKey(
        Subcategory, on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    image = cloudinary.models.CloudinaryField('image', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def final_price(self):
        if hasattr(self, "discount") and self.discount.start_date <= now() <= self.discount.end_date:
            return self.price - (self.price * self.discount.discount_percentage / 100)
        return self.price

    def __str__(self):
        return self.name
