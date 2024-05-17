from django.forms import ValidationError
from django.db import transaction as db_transaction
from rest_framework import viewsets, permissions
from django.utils import timezone

from order.models import Order, OrderItem
from order.serializers import OrderSerializer
from product.models import Variant
from .models import Expense
import csv
import pandas as pd
from datetime import datetime, timedelta
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExpenseSerializer
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import action
from rest_framework import status


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        datetime_value = self.request.data.get('datetime')
        if datetime_value:
            serializer.save(created_by=self.request.user, business=self.request.user.business, created_at=datetime_value)
        else:
            serializer.save(created_by=self.request.user, business=self.request.user.business)



class BulkExpenseUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        csv_file = request.FILES.get('file')
        business_id = request.data.get('business')

        if not csv_file:
            return Response({'error': 'No CSV file provided'}, status=400)

        expenses_to_create = []
        try:
            reader = csv.DictReader(csv_file.read().decode('utf-8').splitlines(), delimiter=',')
            previous_date = None
            for row in reader:
                date_str = row.get('Date')
                description = row.get('Description')
                amount = row.get('Expenses ($)')

                if date_str:
                    date = None
                    # Convert date string to datetime object
                    formats = ['%m/%d/%Y', '%m-%d-%Y', '%Y-%m-%d %H:%M:%S', '%y-%m-%d', '%d-%m-%Y']

                    for format in formats:
                        try:
                            date = datetime.strptime(date_str, format)
                            previous_date = date
                            break  # Break the loop if parsing is successful
                        except ValueError:
                            pass  # Continue to the next format if parsing fails
                    else:
                        if date is None:
                            print("Can't parse this date: ", date_str)
                else:
                    date = previous_date

                # skip this row.
                if date and amount:
                    expense = Expense(datetime=date, notes=description, amount=amount, business_id=business_id)
                    expenses_to_create.append(expense)
                else:
                    print("Expense: Skipped row", row)
            
            if expenses_to_create:
                # Bulk create expenses
                Expense.objects.bulk_create(expenses_to_create)

                return Response({'message': 'Expenses created successfully'}, status=201)
            else:
                return Response({'error': 'kindly check your file content.'}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=400)


class TransactionView(APIView):
    def get(self, request):
        start_time = request.query_params.get('start_time')
        end_time = request.query_params.get('end_time')

        if not start_time or not end_time:
            return Response({'error': 'Both start_time and end_time parameters are required'}, status=400)

        start_datetime = datetime.fromisoformat(start_time)
        end_datetime = datetime.fromisoformat(end_time)

        # added addition one day since end date should be 2024-05-03 00:00:00
        orders = Order.objects.filter(executed_at__gte=start_datetime, executed_at__lte=end_datetime + timedelta(days=1))
        expenses = Expense.objects.filter(created_at__gte=start_datetime, created_at__lte=end_datetime + timedelta(days=1))

        order_serializer = OrderSerializer(orders, many=True)
        expense_serializer = ExpenseSerializer(expenses, many=True)

        return Response({'orders': order_serializer.data, 'expenses': expense_serializer.data})


class RevenueFileUploadAPIView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')

        if not file:
            return Response({'error': 'File should be uploaded to process the request'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if file is an Excel file
        if not file.name.endswith('.xlsx'):
            return Response({'error': 'Please upload a valid Excel file'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            products_df = pd.read_excel(file, sheet_name='Product')
            transactions_df = pd.read_excel(file, sheet_name='Transaction')

            # Replace NaN values with empty strings
            products_df.fillna('', inplace=True)
            transactions_df.fillna('', inplace=True)

            # Convert DataFrames to dictionaries
            products_data = products_df.to_dict(orient='records')
            transactions_data = transactions_df.to_dict(orient='records')

            self.create_orders_and_items(transactions_data, products_data)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'message': 'Revenue file uploaded successfully'}, status=status.HTTP_201_CREATED)


    def create_orders_and_items(self, transaction_data, products_data):
        with db_transaction.atomic():
            for transaction in transaction_data:
                invoice_number = transaction['Invoice Number']
                product_data_list = [product for product in products_data if product['Invoice Number'] == invoice_number]
                payment_type = Order.UNSETTLED if transaction.get('Status') == "Unsettled" else Order.CASH

                total_price = transaction['Grand Total']
                executed_at = datetime.strptime(transaction['Date'], '%Y-%m-%d %H:%M:%S')
                executed_at = timezone.make_aware(executed_at)
                order = Order(
                    id=invoice_number,
                    business=self.request.user.business,
                    status=Order.COMPLETED,
                    total_price=total_price,
                    executed_at=executed_at,
                    payment_type=payment_type
                )
                order.save()

                # Create Order Items
                for product_data in product_data_list:
                    sku = product_data['SKU']
                    if '-' in sku:
                        variant_id = sku
                        try:
                            variant = Variant.objects.get(variant_id=variant_id)
                            product_id = variant.product_id
                        except Variant.DoesNotExist:
                            raise ValidationError("Invalid variant Id: " + variant_id)
                    else:
                        product_id = sku
                        variant = None

                    order_item = OrderItem(
                        order=order,
                        product_id=product_id,
                        variant=variant,
                        sales_price=product_data['Sales Price'],
                        quantity=product_data['Qty'],
                    )
                    order_item.save()
