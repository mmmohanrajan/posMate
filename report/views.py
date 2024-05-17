from rest_framework import generics
from django.db.models import Sum, F
from order.models import OrderItem
from datetime import datetime
from report.serializers import TopProductsSerializer


class TopProductsAPIView(generics.ListAPIView):
    serializer_class = TopProductsSerializer

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date')
        end_date = self.request.query_params.get('end_date')
        top = self.request.query_params.get('top') or 1000
        sort_by = self.request.query_params.get('sort') or "price"

        if not start_date or not end_date:
            return OrderItem.objects.none()

        start_date = datetime.fromisoformat(start_date)
        end_date = datetime.fromisoformat(end_date)

        order_items = OrderItem.objects.filter(
            order__executed_at__date__range=[start_date, end_date]
        ).values(
            'product__name', 'product__unit', 'variant__name', 'variant__unit', 'product__category__name', 'sales_price'
        ).annotate(
            total_quantity=Sum('quantity'),
            total_amount=F('sales_price') * F('total_quantity')
        )

        if sort_by == 'quantity':
            order_items = order_items.order_by('-total_quantity')[:top]
        elif sort_by == 'price':
            order_items = order_items.order_by('-total_amount')[:top]

        return order_items


