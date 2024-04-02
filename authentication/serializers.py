from django.forms import ValidationError
from django.contrib.auth import authenticate
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from authentication.models import User
from django.contrib.auth.password_validation import validate_password


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)

    def validate(self, attrs):
        username_or_email = attrs.get('username')
        password = attrs.get('password')

        # Check if input is an email
        if '@' in username_or_email:
            # Authenticate using email
            user = authenticate(email=username_or_email, password=password)
        else:
            # Authenticate using username
            user = authenticate(username=username_or_email, password=password)

        if user:
            attrs['user'] = user
            return attrs
        else:
            raise AuthenticationFailed('Invalid credentials')


class UserRegistrationSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=128)
    confirm_password = serializers.CharField(max_length=128)

    def validate(self, data):
        """
        Check that the username and email are unique.
        Also validate that the password and confirm password match.
        """
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        confirm_password = data.get('confirm_password')
        
        if User.objects.filter(username=username).exists():
            raise serializers.ValidationError({'username': 'Username already exists'})

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'Email already exists'})

        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match'})

        try:
            # Validate password strength using Django's validators
            validate_password(password)
        except ValidationError as e:
            # If the password does not meet strength requirements, raise a validation error
            raise serializers.ValidationError({'password': list(e.messages)})

        return data

    def create(self, validated_data):
        """
        Create and return a new user instance.
        """
        username = validated_data['username']
        email = validated_data['email']
        password = validated_data['password']
        
        user = User.objects.create_user(username=username, email=email, password=password)
        return user
