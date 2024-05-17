from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BulkExpenseUploadAPIView, ExpenseViewSet, TransactionView, RevenueFileUploadAPIView

router = DefaultRouter()
router.register(r'expense', ExpenseViewSet)

urlpatterns = [
    path('expense/bulk-upload/', BulkExpenseUploadAPIView.as_view(), name='bulk_expense_upload'),
    path('', include(router.urls)),
    path('transactions/', TransactionView.as_view()),
    path('revenue/file-upload/', RevenueFileUploadAPIView.as_view(), name='revenue_file_upload'),
]
