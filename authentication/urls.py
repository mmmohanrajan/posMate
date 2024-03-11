from django.urls import path
from .views import user_login, user_logout, register_user

urlpatterns = [
    path('login/', user_login, name='user_login'),
    path('logout/', user_logout, name='user_logout'),
    path('register/', register_user, name='user_register'),
]
