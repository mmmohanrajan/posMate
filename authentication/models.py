from django.contrib.auth.models import AbstractUser
from core.models import Business


class User(AbstractUser):

    class Meta:
        app_label = 'authentication'
    
    @property
    def business(self):
        return Business.objects.get(owners=self)
