from django.contrib import admin

from order.models import Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'status', 'total_price', 'executed_at', 'created_at']

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
