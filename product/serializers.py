from rest_framework import serializers
from .models import Product, Variant

class VariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Variant
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    variants = VariantSerializer(many=True, read_only=True)  # Serializer for variants

    class Meta:
        model = Product
        fields = ['id', 'name', 'barcode', 'category', 'sales_price', 'product_cost', 'stock', 'warning_limit', 'unit', 'featured', 'unlimited', 'image', 'variants']
