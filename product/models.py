from django.db import models

from core.models import Business

class Product(models.Model):
    id = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=100)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=50, blank=True)
    category = models.CharField(max_length=50)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    warning_limit = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)
    featured = models.BooleanField(default=False)
    unlimited = models.BooleanField(default=False)
    image = models.ImageField(upload_to='product_images/', blank=True)

    def __str__(self):
        return self.name

class Variant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    name = models.CharField(max_length=100)
    variant_id = models.CharField(max_length=20, unique=True)
    barcode = models.CharField(max_length=50, blank=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2)
    product_cost = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    warning_limit = models.IntegerField(default=0)
    unit = models.CharField(max_length=20)
    unlimited = models.BooleanField(default=False)
    image = models.ImageField(upload_to='variant_images/', blank=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"
