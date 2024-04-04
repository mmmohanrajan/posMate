
from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'name', 'business', 'amount', 'qty', 'payment_type', 'created_by', 'created_at']
        read_only_fields = ['created_by', 'id', 'business']
