from rest_framework import viewsets, permissions
from .models import Expense
import csv
from datetime import datetime
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import ExpenseSerializer
from .permissions import CanCreateExpenseForBusiness, IsOwnerOrReadOnly

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated, CanCreateExpenseForBusiness]

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwnerOrReadOnly()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


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
                    # Convert date string to datetime object
                    date = datetime.strptime(date_str, '%m/%d/%Y')
                    previous_date = date
                else:
                    date = previous_date

                # skip this row.
                if date and amount:
                    expense = Expense(datetime=date, notes=description, amount=amount, business_id=business_id)
                    expenses_to_create.append(expense)
                else:
                    print("Skipped row", row)
            
            if expenses_to_create:
                # Bulk create expenses
                Expense.objects.bulk_create(expenses_to_create)

                return Response({'message': 'Expenses created successfully'}, status=201)
            else:
                return Response({'error': 'kindly check your file content.'}, status=400)

        except Exception as e:
            return Response({'error': str(e)}, status=400)