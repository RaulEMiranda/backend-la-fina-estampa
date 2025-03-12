from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.serializers.PaymentSerializer import PaymentSerializer
from api.model.PaymentModel import Payment
from api.model.OrderModel import Order
from rest_framework.exceptions import ValidationError

# 📌 1. Crear un pago (Solo usuario autenticado)
@extend_schema(
    summary="Registrar un pago",
    description="Permite a un usuario registrar el pago de una orden. No se puede duplicar el pago de una orden.",
    request=PaymentSerializer,
    responses={201: PaymentSerializer, 400: OpenApiResponse(description="Datos inválidos")}
)
class PaymentCreateView(generics.CreateAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.validated_data.get('order')
        if Payment.objects.filter(order=order).exists():
            raise ValidationError({"detail": "Esta orden ya tiene un pago registrado."})
        serializer.save()

# 📌 2. Listar pagos (Solo admins pueden ver todos los pagos)
@extend_schema(
    summary="Listar pagos",
    description="Devuelve una lista de todos los pagos. Solo accesible por administradores.",
    responses={200: PaymentSerializer(many=True)}
)
class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [IsAdminUser]  # Solo administradores

    def get_queryset(self):
        return Payment.objects.all()
