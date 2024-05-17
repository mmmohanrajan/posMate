from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem, Variant
from django.utils import timezone


class OrderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.data
        items = payload.get('items', [])
        total_price = payload.get('total_price')
        
        order = Order.objects.create(
            id=Order.generate_order_id(),
            business=request.user.business,
            total_price=total_price,
            status=Order.COMPLETED,
            created_by=request.user,
            executed_at=timezone.now()
        )
        order.save()
        
        for item_data in items:
            product_id = item_data.get('product') or item_data.get('id')
            variant_id = item_data.get('variant_id')
            order_count = int(item_data.get('order_count', 0))

            order_item_data = {
                'product_id': product_id,
                'quantity': order_count,
                'sales_price': item_data.get('sales_price', 0)
            }

            if variant_id:
                try:
                    variant = Variant.objects.get(variant_id=variant_id)
                except Variant.DoesNotExist:
                    return Response({'message': 'invalid varint ID'}, status=status.HTTP_400_BAD_REQUEST) 
                order_item_data.update(variant=variant)

            OrderItem.objects.create(order=order, **order_item_data)
        return Response({'message': 'Order created successfully', 'order_id': order.id, 'amount': total_price}, status=status.HTTP_201_CREATED)
