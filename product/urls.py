# urls.py
from django.urls import path
from .views import BulkUploadAPI, ProductListAPIView

urlpatterns = [
    path('product/bulk-upload/', BulkUploadAPI.as_view(), name='bulk_upload'),
    path('products/', ProductListAPIView.as_view(), name='product-list'),
]