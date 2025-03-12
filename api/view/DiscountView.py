from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser
from drf_spectacular.utils import extend_schema
from django.utils.timezone import now
from api.serializers.DiscountSerializer import DiscountSerializer
from api.model.DiscountModel import Discount


# 📌 1. Listar descuentos activos
@extend_schema(
    summary="Listar descuentos activos",
    description="Devuelve una lista de todos los descuentos vigentes en productos.",
    responses={200: DiscountSerializer(many=True)}
)
class DiscountListView(generics.ListAPIView):
    """
    API para listar descuentos activos.
    Cualquier usuario puede acceder a esta lista.
    """
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Discount.objects.filter(start_date__lte=now(), end_date__gte=now())


# 📌 2. Obtener los detalles de un descuento específico
@extend_schema(
    summary="Obtener detalles de un descuento",
    description="Devuelve los detalles de un descuento en un producto específico.",
    responses={200: DiscountSerializer, 404: {"detail": "Descuento no encontrado"}}
)
class DiscountRetrieveView(generics.RetrieveAPIView):
    """
    API para obtener un descuento específico.
    """
    serializer_class = DiscountSerializer
    permission_classes = [AllowAny]
    queryset = Discount.objects.all()


# 📌 3. Crear un nuevo descuento (Solo Admins)
@extend_schema(
    summary="Crear un nuevo descuento",
    description="Permite a un administrador registrar un nuevo descuento para un producto.",
    request=DiscountSerializer,
    responses={201: DiscountSerializer, 400: {"detail": "Datos inválidos"}}
)
class DiscountCreateView(generics.CreateAPIView):
    """
    API para crear un nuevo descuento.
    Solo los administradores pueden acceder.
    """
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser]


# 📌 4. Actualizar un descuento (Solo Admins)
@extend_schema(
    summary="Actualizar un descuento",
    description="Permite a un administrador modificar los datos de un descuento existente.",
    request=DiscountSerializer,
    responses={200: DiscountSerializer, 400: {"detail": "Datos inválidos"}, 404: {"detail": "Descuento no encontrado"}}
)
class DiscountUpdateView(generics.UpdateAPIView):
    """
    API para actualizar un descuento existente.
    Solo los administradores pueden acceder.
    """
    serializer_class = DiscountSerializer
    permission_classes = [IsAdminUser]
    queryset = Discount.objects.all()


# 📌 5. Eliminar un descuento (Solo Admins)
@extend_schema(
    summary="Eliminar un descuento",
    description="Permite a un administrador eliminar un descuento existente.",
    responses={204: None, 404: {"detail": "Descuento no encontrado"}}
)
class DiscountDeleteView(generics.DestroyAPIView):
    """
    API para eliminar un descuento.
    Solo los administradores pueden acceder.
    """
    permission_classes = [IsAdminUser]
    queryset = Discount.objects.all()
