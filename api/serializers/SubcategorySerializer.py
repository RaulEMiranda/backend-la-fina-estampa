from rest_framework import serializers
from .CategorySerializer import CategorySerializer
from api.models import Category, Subcategory


class SubcategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), source='category', write_only=True)

    class Meta:
        model = Subcategory
        fields = ['id', 'name', 'category', 'category_id']
