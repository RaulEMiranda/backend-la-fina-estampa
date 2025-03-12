from rest_framework import serializers
from api.models import Product, Category, Subcategory
from drf_spectacular.utils import extend_schema_field

class ProductSerializer(serializers.ModelSerializer):
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all())
    subcategory = serializers.PrimaryKeyRelatedField(queryset=Subcategory.objects.all(), allow_null=True)  # Permite que sea opcional
    image = serializers.ImageField(required=False)  # Permite subir archivos
    final_price = serializers.SerializerMethodField()  # Agregamos el precio final

    class Meta:
        model = Product
        fields = '__all__'  # Esto incluye `final_price` automáticamente

    @extend_schema_field(serializers.FloatField())  # Define el tipo de retorno para Spectacular
    def get_final_price(self, obj) -> float:
        return obj.final_price()  # Llamamos al método del modelo
