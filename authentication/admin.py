from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from authentication.models import User

# Define the custom user admin class
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2'),
        }),
    )

admin.site.register(User, CustomUserAdmin)
