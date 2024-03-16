from django.contrib import admin

from product.models import Product, Variant

# Register your models here.

admin.site.register(Product)
admin.site.register(Variant)
