"""
URL configuration for uderzoai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from core.views import frontpage, registration, dashboard, fleet, routes, stops, login_user, logout_user, register_user
from core.views import activation_success, reset_password
from core.views import addproduct
from core.views import addcompany
from core.api import api
from core.views import CustomTokenObtainPairView
from core.views import ActivateUser
from core.views import StopCreateView
from crudbuilder import urls
from core import views

from rest_framework_simplejwt.views import TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('crud/',  include(urls)),
    path('api/', api.urls),
    path('', frontpage, name='frontpage'),
    path('dashboard/', dashboard, name='dashboard'),
    path('fleet/', fleet, name='fleet'),
    path('routes/', routes, name='routes'),
    path('stops/', StopCreateView.as_view(), name='stops'),
    path('addproduct/', addproduct, name='addproduct'),
    path('addcompany/', addcompany, name='addcompany'),
    # path('addstop/', addstop, name='addstop'),
    path('registration/', registration, name='registration'),
    # Deprecated signin
    # path('signin/', signin, name='signin'),
    path('login/', login_user, name="login"),
    path('register/', register_user, name="register"),
    path('logout/', logout_user, name="logout"),
    # path('members/', include('django.contrib.auth.urls')),
    # path('members/', include('members.urls')),
    path("__reload__/", include("django_browser_reload.urls")),
    path('activate/', include('core.urls')),
    path('auth/jwt/create/',CustomTokenObtainPairView.as_view(),name='custom_jwt_create'),
    path('auth/jwt/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('accounts/activate/<uid>/<token>', ActivateUser.as_view({'get': 'activation'}), name='activation'),
    path('activation/success/', activation_success, name='activation_success'),
    path('auth/reset_password/', reset_password, name='reset_password'),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    
    # products
    path('products/', include(('core.urls_products', 'core'), namespace='products')),
    path("__debug__/", include("debug_toolbar.urls")),
    
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# if settings.DEBUG:
#    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_title = "FR8 Pro Admin"
admin.site.site_header = "FR8 Pro Platform"
admin.site.index_title = "FR8 Pro Administration"
