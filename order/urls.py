from django.urls import path
from .views import OrderAPIView

urlpatterns = [
    path('order/', OrderAPIView.as_view(), name='order-api'),  # Define the URL route for the OrderAPIView
]