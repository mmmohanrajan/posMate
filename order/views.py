from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Order, OrderItem, Product, Variant
from .serializers import OrderItemSerializer
from decimal import Decimal


class OrderAPIView(APIView):
    def post(self, request, *args, **kwargs):
        payload = request.data
        items = payload.get('items', [])
        total_price = payload.get('total_price')
        
        order = Order.objects.create(
            business=request.user.business,
            total_price=total_price,
            status=Order.COMPLETED,
            created_by=request.user
        )
        order.save()
        
        for item_data in items:
            print(item_data)
            
            product_id = item_data.get('product') or item_data.get('id')
            variant_id = item_data.get('variant_id')
            order_count = int(item_data.get('order_count', 0))

            print(product_id)

            order_item_data = {
                'product_id': product_id,
                'quantity': order_count,
            }

            if variant_id:
                try:
                    variant = Variant.objects.get(variant_id=variant_id)
                except Variant.DoesNotExist:
                    return Response({'message': 'invalid varint ID'}, status=status.HTTP_400_BAD_REQUEST) 
                order_item_data.update(variant=variant)

            OrderItem.objects.create(order=order, **order_item_data)

            # serializer = OrderItemSerializer(data=order_item_data)
            # if serializer.is_valid():
            #     serializer.save()
            # else:
            #     return Response({'message': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Order created successfully', 'order_id': order.id, 'amount': total_price}, status=status.HTTP_201_CREATED)
