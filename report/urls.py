from django.urls import path
from .views import TopProductsAPIView

urlpatterns = [
    path('report/top-products/', TopProductsAPIView.as_view(), name='top-products'),
]
