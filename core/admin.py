from django.contrib import admin
from .models import Business, Expense

class BusinessAdmin(admin.ModelAdmin):
    pass

admin.site.register(Business, BusinessAdmin)
admin.site.register(Expense)