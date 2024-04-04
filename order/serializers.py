from rest_framework import serializers

from product.models import Product
from .models import Order, OrderItem


class OrderItemSerializer(serializers.ModelSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    
    class Meta:
        model = OrderItem
        fields = ['order', 'product_id', 'variant_id', 'quantity']

    def validate(self, attrs):
        # Ensure that the product_id is valid
        product_id = attrs.get('product_id')
        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            raise serializers.ValidationError("Invalid product_id")

        # Ensure that the variant_id is valid if provided
        variant_id = attrs.get('variant_id')
        if variant_id:
            if not product.variants.filter(variant_id=variant_id).exists():
                raise serializers.ValidationError("Invalid variant_id")

        # Ensure that the order_count is not zero
        order_count = attrs.get('quantity')
        if order_count < 1:
            raise serializers.ValidationError("Order count cannot be zero")

        return attrs
    

class OrderSerializer(serializers.ModelSerializer):
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = '__all__'

    def get_items_count(self, obj):
        return obj.items.count()