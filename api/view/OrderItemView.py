from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, OpenApiParameter
from api.serializers.OrderItemSerializer import OrderItemSerializer
from api.model.OrderItemModel import OrderItem
from api.model.OrderModel import Order

# 📌 1. Listar todos los items de una orden
@extend_schema(
    summary="Listar los productos de una orden",
    description="Devuelve una lista de todos los productos que pertenecen a una orden específica.",
    parameters=[OpenApiParameter(name="order_id", description="ID de la orden", required=True, type=int)],
    responses={200: OrderItemSerializer(many=True), 404: {"detail": "Orden no encontrada"}}
)
class OrderItemListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        try:
            order = Order.objects.get(id=order_id, customer=request.user.customer)
            items = order.items.all()
            serializer = OrderItemSerializer(items, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Order.DoesNotExist:
            return Response({"detail": "Orden no encontrada"}, status=status.HTTP_404_NOT_FOUND)

# 📌 2. Obtener los detalles de un OrderItem específico
@extend_schema(
    summary="Obtener detalles de un OrderItem",
    description="Devuelve la información detallada de un producto en una orden.",
    parameters=[OpenApiParameter(name="item_id", description="ID del OrderItem", required=True, type=int)],
    responses={200: OrderItemSerializer, 404: {"detail": "Item no encontrado"}}
)
class OrderItemRetrieveView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, item_id):
        try:
            item = OrderItem.objects.get(id=item_id, order__customer=request.user.customer)
            serializer = OrderItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Item no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# 📌 3. Agregar un producto a una orden
@extend_schema(
    summary="Agregar un producto a una orden",
    description="Permite agregar un producto a una orden específica.",
    request=OrderItemSerializer,
    responses={201: OrderItemSerializer, 400: {"detail": "Datos inválidos"}}
)
class OrderItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = OrderItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 📌 4. Modificar la cantidad de un producto en una orden
@extend_schema(
    summary="Actualizar un OrderItem",
    description="Permite modificar la cantidad de un producto dentro de una orden.",
    request=OrderItemSerializer,
    responses={200: OrderItemSerializer, 400: {"detail": "Datos inválidos"}, 404: {"detail": "Item no encontrado"}}
)
class OrderItemUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, item_id):
        try:
            item = OrderItem.objects.get(id=item_id, order__customer=request.user.customer)
            serializer = OrderItemSerializer(item, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Item no encontrado"}, status=status.HTTP_404_NOT_FOUND)

# 📌 5. Eliminar un producto de una orden
@extend_schema(
    summary="Eliminar un producto de una orden",
    description="Permite eliminar un producto específico de una orden.",
    responses={204: None, 404: {"detail": "Item no encontrado"}}
)
class OrderItemDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, item_id):
        try:
            item = OrderItem.objects.get(id=item_id, order__customer=request.user.customer)
            item.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except OrderItem.DoesNotExist:
            return Response({"detail": "Item no encontrado"}, status=status.HTTP_404_NOT_FOUND)
