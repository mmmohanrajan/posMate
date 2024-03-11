
from rest_framework import serializers
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ['id', 'business', 'user', 'amount', 'notes', 'payment', 'datetime']
        read_only_fields = ['user']

    def validate(self, data):
        """
        Ensure that required fields are provided.
        """
        if not data.get('amount'):
            raise serializers.ValidationError({'amount': 'This field is required.'})

        if not data.get('datetime'):
            raise serializers.ValidationError({'datetime': 'This field is required.'})

        return data
 
