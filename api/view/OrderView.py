from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiResponse
from api.serializers.OrderSerializer import OrderSerializer
from api.model.OrderModel import Order

@extend_schema(
    summary="Crea una nueva orden",
    description="Permite a cualquier usuario autenticado crear una nueva orden.",
    request=OrderSerializer,
    responses={
        201: OrderSerializer,
        400: OpenApiResponse(description="Los datos proporcionados no son válidos"),
    }
)
class OrderCreateView(generics.CreateAPIView):
    """
    API para crear una nueva orden.
    Cualquier usuario autenticado puede realizar una compra.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user.customer)

@extend_schema(
    summary="Lista las órdenes del usuario",
    description="Obtiene la lista de órdenes del usuario autenticado, ordenadas por fecha de creación.",
    responses={200: OrderSerializer(many=True)}
)
class OrderListView(generics.ListAPIView):
    """
    API para listar órdenes.  
    Cada usuario solo puede ver sus propias compras.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer).order_by('-created_at')

@extend_schema(
    summary="Obtiene una orden específica",
    description="Permite a un usuario autenticado ver los detalles de una orden específica. No se permite la edición ni eliminación.",
    responses={
        200: OrderSerializer,
        403: OpenApiResponse(description="No autorizado"),
        404: OpenApiResponse(description="Orden no encontrada"),
    }
)
class OrderDetailView(generics.RetrieveAPIView):
    """
    API para ver una orden específica.  
    No se permite modificar ni eliminar.
    """
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user.customer)
