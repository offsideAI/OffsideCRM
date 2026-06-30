"""URL configuration for the OffsideVentures project (JSON API + admin + auth)."""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenBlacklistView

from core.api import api
from core.views import (
    ActivateUser,
    CustomTokenObtainPairView,
    activation_success,
    api_root,
)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", api.urls),
    path("", api_root, name="api_root"),

    # Auth — JWT + Djoser
    path("auth/jwt/create/", CustomTokenObtainPairView.as_view(), name="custom_jwt_create"),
    path("auth/jwt/blacklist/", TokenBlacklistView.as_view(), name="token_blacklist"),
    path("accounts/activate/<uid>/<token>", ActivateUser.as_view({"get": "activation"}), name="activation"),
    path("activation/success/", activation_success, name="activation_success"),
    path("auth/", include("djoser.urls")),
    path("auth/", include("djoser.urls.jwt")),
    path("activate/", include("core.urls")),
]

if settings.DEBUG:
    urlpatterns += [path("__reload__/", include("django_browser_reload.urls"))]
    try:
        import debug_toolbar  # noqa: F401

        urlpatterns += [path("__debug__/", include("debug_toolbar.urls"))]
    except ImportError:
        pass
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin branding
admin.site.site_title = "OffsideVentures"
admin.site.site_header = "OffsideVentures"
admin.site.index_title = "Administration"
