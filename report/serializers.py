from rest_framework import serializers

class TopProductsSerializer(serializers.Serializer):
    product_name = serializers.CharField(source='product__name')
    product_unit = serializers.CharField(source='product__unit')
    variant_name = serializers.CharField(source='variant__name', allow_null=True)
    variant_unit = serializers.CharField(source='variant__unit', allow_null=True)
    product_category_name = serializers.CharField(source='product__category__name')
    total_quantity = serializers.IntegerField()
    sales_price = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_amount = serializers.DecimalField(max_digits=10, decimal_places=2)
