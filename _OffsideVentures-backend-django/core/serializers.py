"""DRF serializers used by Djoser for auth/user endpoints (`/auth/...`).

The CRM resources themselves are served by Django Ninja (see core/api.py); these
serializers only cover registration, the current-user payload, and JWT claims.
"""
from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import Profile

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'first_name', 'last_name', 'email']


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['role', 'job_title', 'phone', 'avatar_url', 'bio']


class UserSerializer(BaseUserSerializer):
    profile = ProfileSerializer(read_only=True)

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            'id',
            'first_name',
            'last_name',
            'email',
            'username',
            'is_active',
            'is_deactivated',
            'profile',
        ]

    def validate(self, attrs):
        validated = super().validate(attrs)
        # Guard deactivated/inactive accounts on the /auth/users/me path.
        request = self.context.get('request')
        user = getattr(request, 'user', None)
        if user is not None and user.is_authenticated:
            if user.is_deactivated:
                raise ValidationError('Account deactivated')
            if not user.is_active:
                raise ValidationError('Account not activated')
        return validated


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user
        data.update({
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'username': user.username,
            'is_active': user.is_active,
            'is_deactivated': user.is_deactivated,
        })
        return data
