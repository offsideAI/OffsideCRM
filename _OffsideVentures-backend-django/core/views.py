"""Thin views for the OffsideVentures backend.

The CRM UI is the separate SvelteKit app; Django serves the JSON API
(see core/api.py), the admin, and JWT/Djoser auth. These views only cover a few
auth helpers and a JSON API root.
"""
from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import redirect
from djoser.views import UserViewSet
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer

User = get_user_model()


def api_root(request):
    return JsonResponse({
        "name": "OffsideVentures API",
        "status": "ok",
        "docs": "/api/docs",
        "openapi": "/api/openapi.json",
        "admin": "/admin/",
    })


@api_view(["POST"])
@permission_classes([AllowAny])
def check_email_exists(request):
    email = request.data.get("email")
    if not email:
        return Response({"error": "Bad_request"}, status=status.HTTP_400_BAD_REQUEST)
    exists = User.objects.filter(email=email).exists()
    return Response(
        {"email_exists": exists},
        status=status.HTTP_200_OK if exists else status.HTTP_404_NOT_FOUND,
    )


@api_view(["POST"])
@permission_classes([AllowAny])
def check_username_exists(request):
    username = request.data.get("username")
    if not username:
        return Response({"error": "Bad_request"}, status=status.HTTP_400_BAD_REQUEST)
    exists = User.objects.filter(username=username).exists()
    return Response(
        {"username_exists": exists},
        status=status.HTTP_200_OK if exists else status.HTTP_404_NOT_FOUND,
    )


@api_view(["GET"])
@permission_classes([AllowAny])
def home(request):
    return Response({"detail": "API status green"}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        user = User.objects.filter(email=request.data.get("email")).first()
        if user is not None:
            if not user.is_active:
                return Response({"detail": "Account not activated"}, status=status.HTTP_401_UNAUTHORIZED)
            if user.is_deactivated:
                return Response({"detail": "Account deactivated"}, status=status.HTTP_401_UNAUTHORIZED)
        return super().post(request, *args, **kwargs)


class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault("context", self.get_serializer_context())
        kwargs["data"] = {"uid": self.kwargs["uid"], "token": self.kwargs["token"]}
        return serializer_class(*args, **kwargs)

    def activation(self, request, uid, token, *args, **kwargs):
        response = super().activation(request, *args, **kwargs)
        if response.status_code == status.HTTP_204_NO_CONTENT:
            return redirect("activation_success")
        return response


def activation_success(request):
    return JsonResponse({"detail": "Account activated successfully"})
