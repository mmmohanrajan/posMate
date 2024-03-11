from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            email = kwargs.get("email")
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            user = super().authenticate(request, username=username, password=password, **kwargs)
        if user and user.check_password(password):
            return user
        return None
