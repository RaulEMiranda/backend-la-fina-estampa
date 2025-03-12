from rest_framework import serializers
from api.model.DiscountModel import Discount

class DiscountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Discount
        fields = '__all__'
