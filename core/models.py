from django.utils import timezone
from django.db import models


class Business(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)  # Physical address of the business
    phone_number = models.CharField(max_length=15, blank=True)  # Contact number for the business
    email = models.EmailField(blank=True)  # Email address for the business
    owners = models.ManyToManyField('authentication.User', related_name='owned_businesses')  # Many-to-Many relationship with owners
    managers = models.ManyToManyField('authentication.User', related_name='managed_businesses', blank=True)  # Many-to-Many relationship with managers
    staff = models.ManyToManyField('authentication.User', related_name='assigned_businesses', blank=True)  # Many-to-Many relationship with staff members

    def __str__(self):
        return self.name


class Expense(models.Model):
    CASH = 'cash'
    CARD = 'card'
    UPI = 'upi'
    PAYMENT_CHOICES = [
        (CASH, 'Cash'),
        (CARD, 'Card'),
        (UPI, 'UPI'),
    ]

    business = models.ForeignKey(Business, on_delete=models.CASCADE, related_name="expense")
    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, null=True, blank=True)  # ForeignKey to User model
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    notes = models.TextField(blank=True)
    payment = models.CharField(max_length=255, choices=PAYMENT_CHOICES, default=CASH)
    datetime = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.user:
            return f"Expense for {self.business.name} - {self.amount} by {self.user.username}"
        else:
            return f"Expense for {self.business.name} - {self.amount}"
