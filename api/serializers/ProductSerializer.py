from rest_framework import serializers
from api.models import Product, Category, Subcategory
from django.core.files.uploadedfile import InMemoryUploadedFile
from PIL import Image
from io import BytesIO
import cloudinary
from cloudinary.models import CloudinaryField
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

    def validate_image(self, value):
        """
        Comprimir la imagen para reducir su tamaño sin perder calidad significativa
        antes de enviarla a Cloudinary.
        """
        if value:
            # Abrir la imagen con Pillow
            img = Image.open(value)

            # Comprobar si la imagen tiene transparencia (canal alfa)
            if img.mode == "RGBA":
                # Crear un fondo blanco (o gris claro) para las áreas transparentes
                # Crea una nueva imagen RGB con el color de fondo deseado (gris claro)
                background = Image.new("RGB", img.size, (242, 244, 251))  # Gris claro (RGB: 240, 240, 240)
                background.paste(img, (0, 0), img)  # Pega la imagen original sobre el fondo

                # Usar la imagen con el fondo en lugar de la original
                img = background

            # Comprimir la imagen manteniendo la calidad
            img_io = BytesIO()
            img.save(img_io, format='JPEG', quality=85)  # Ajusta la calidad según sea necesario
            img_io.seek(0)

            # Crear un nuevo archivo de memoria con la imagen comprimida
            file_name = value.name.split('.')[0] + '.jpg'  # Convertir a JPG si no lo es
            image_file = InMemoryUploadedFile(img_io, None, file_name, 'image/jpeg', img_io.getbuffer().nbytes, None)

            return image_file
        return value
