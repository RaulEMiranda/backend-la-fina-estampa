from django.contrib import admin
from .models import Product
from cloudinary.forms import CloudinaryFileField

class ProductAdmin(admin.ModelAdmin):
    formfield_overrides = {
        Product.image.field: {'widget': CloudinaryFileField},
    }

admin.site.register(Product, ProductAdmin)