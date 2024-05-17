import datetime
import random
import string
from django.db import models
from django.contrib.auth import get_user_model
from core.models import Business
from product.models import Product, Variant


class Order(models.Model):
    PENDING = 'pending'
    CONFIRMED = 'confirmed'
    SHIPPED = 'shipped'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    ORDER_STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (CONFIRMED, 'Confirmed'),
        (SHIPPED, 'Shipped'),
        (CANCELLED, 'Cancelled'),
        (COMPLETED, 'Completed')
    ]

    CASH = 'cash'
    UPI = 'upi'
    UNSETTLED = 'unsettled'
    PAYMENT_TYPES = [
        (CASH, 'Cash'),
        (UPI, 'UPI'),
        (UNSETTLED, 'Unsettled'),
    ]

    def generate_order_id():
        current_date = datetime.date.today()
        formatted_date = current_date.strftime("%Y%m%d")
        random_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        random_string_with_hyphen = '-'.join([random_string[:3], random_string[3:]])
        order_id = f"{formatted_date}/{random_string_with_hyphen}"
        return order_id

    id = models.CharField(primary_key=True, max_length=50)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="orders")
    created_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True, blank=True)
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES, default=PENDING)
    payment_type = models.CharField(max_length=20, choices=PAYMENT_TYPES, default=CASH)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    executed_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Order ID: {self.id}, Status: {self.status}, Total Price: {self.total_price}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    variant = models.ForeignKey(Variant, on_delete=models.CASCADE, null=True, blank=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField()

    def __str__(self):
        return f"Order Item - Order ID: {self.order.id}, Product: {self.product}, Variant: {self.variant}, Quantity: {self.quantity}"
