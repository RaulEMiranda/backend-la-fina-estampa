from rest_framework import serializers
from api.models import Order
from .OrderItemSerializer import OrderItemSerializer


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(
        many=True, read_only=True)  # Relación con OrderItem

    class Meta:
        model = Order
        fields = '__all__'
