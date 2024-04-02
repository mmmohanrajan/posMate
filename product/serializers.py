from rest_framework import serializers
from .models import Product, Variant, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name')  # Fields to include in the serialized Category data


class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)  # Nested serializer for Category
    variants = VariantSerializer(many=True, read_only=True)  # Serializer for variants

    class Meta:
        model = Product
        fields = ['id', 'name', 'barcode', 'category', 'sales_price', 'product_cost', 'stock', 'warning_limit', 'unit', 'featured', 'unlimited', 'image', 'variants']
