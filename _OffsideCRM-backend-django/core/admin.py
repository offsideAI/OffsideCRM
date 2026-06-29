from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import CustomUser
from unfold.admin import ModelAdmin
from django.contrib.admin.helpers import AdminField
from .models import Property
from .models import PropertyType
from .models import PropertyStatus
from .models import Profile
from .models import Category
from .models import Dataset
from .models import Service
from .models import Cat
from .models import Product
from .models import Country
from .models import StateProvince
from .models import Address
from .models import Company
from .models import Load
from .models import Location
from .models import Device
from .models import Stop
from .models import Route
from .models import EVChargingLocation
from .models import TruckType

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Profile)
# admin.site.register(PropertyType)
# admin.site.register(PropertyStatus)
# admin.site.register(Property)
admin.site.register(Category)
admin.site.register(Dataset)
admin.site.register(Service)
admin.site.register(Cat)
admin.site.register(Product)
admin.site.register(Country)
admin.site.register(StateProvince)
admin.site.register(Address)
admin.site.register(Company)
admin.site.register(Load)
admin.site.register(Location)
admin.site.register(Device)
admin.site.register(Stop)
admin.site.register(Route)
admin.site.register(EVChargingLocation)
admin.site.register(TruckType)



# PropertyTypeAdmin
#class PropertyTypeAdmin(ModelAdmin):
#    list_display = ('id', 'name', 'description')
#    search_fields = ('id', 'name', 'description')
#    list_filter = ('id', 'name', 'description')
#    list_per_page = 100
    
# PropertyStatusAdmin
#class PropertyStatusAdmin(ModelAdmin):
#    list_display = ('id', 'name', 'description')
#    search_fields = ('id', 'name', 'description')
#    list_filter = ('id', 'name', 'description')
#    list_per_page = 100


# PropertyAdmin
#class PropertyAdmin(ModelAdmin):
#    list_display = ('name', 'date_published')
#    search_fields = ('name', 'date_published')
#    list_filter = ('name', 'date_published')
#    list_per_page = 100

# CustomUser
class CustomUserAdmin(UserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "email", "first_name", "last_name", "password1", "password2"),
            },
        ),
    )
    list_display = ('id', 'username', 'email', 'is_staff', 'is_active', 'is_deactivated', 'is_superuser', 'date_joined', 'last_login')

# Profile Inline
class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

# Profile
class ProfileAdmin(ModelAdmin):
    list_display = ('userid', 'handle', 'truck_type', 'capacity', 'license_number', 'status', 'base_location')
    list_per_page = 100
    
# ... (existing code)

# admin.site.unregister(CustomUser)
admin.site.unregister(CustomUser)

# admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(CustomUser)
class UserAdmin(CustomUserAdmin, ModelAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)
    
# Category
class CategoryAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    list_per_page = 100

# Dataset
class DatasetAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    list_per_page = 100

# Service
class ServiceAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    list_per_page = 100
    
# Cat
class CatAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    list_per_page = 100
 
# Product
class ProductAdmin(ModelAdmin):
    list_display = ('name', 'created_at')
    list_per_page = 100
    
# Country
class CountryAdmin(ModelAdmin):
    list_display = ('name', 'iso_code')
    list_per_page = 100
    
# StateProvince
class StateProvinceAdmin(ModelAdmin):
    list_display = ('name', 'iso_code')
    list_per_page = 100
    
# Address
class AddressAdmin(ModelAdmin):
    list_display = (
        'address_line1', 
        'postal_code',
        'address_notes',
        )
    list_per_page = 100
   
# Company
class CompanyAdmin(ModelAdmin):
    list_display = ('name', 'desc')
    list_per_page = 100
    
# Load
class LoadAdmin(ModelAdmin):
   list_display = ('title', 'origin_pickup_range_start', 'destination_dropoff_range_start', 'load_assigned_to_user') 
   list_per_page = 100

# Location
class LocationAdmin(ModelAdmin):
   list_display = ('name', 'slug')
   list_per_page = 100
    
# Device
class DeviceAdmin(ModelAdmin):
   list_display = ('name', 'slug')
   list_per_page = 100


# Stop
class StopAdmin(ModelAdmin):
   list_display = ('title', 'description')
   list_per_page = 100
   
# Route
class RouteAdmin(ModelAdmin):
   list_display = ('title', 'slug')
   list_per_page = 100
    
# EVChargingLocation
class EVChargingLocationAdmin(ModelAdmin):
   list_display = ('station_name', 'station_address')
   list_per_page = 100
    
# admin.site.unregister(PropertyType)
# admin.site.register(PropertyType, PropertyTypeAdmin)

# admin.site.unregister(PropertyStatus)
# admin.site.register(PropertyStatus, PropertyStatusAdmin)

# admin.site.unregister(Property)
# admin.site.register(Property, PropertyAdmin)

# admin.site.unregister(CustomUser)
admin.site.unregister(CustomUser)

# admin.site.register(CustomUser, CustomUserAdmin)
@admin.register(CustomUser)
class UserAdmin(CustomUserAdmin, ModelAdmin):
    inlines = (ProfileInline,)


admin.site.unregister(Profile)
admin.site.register(Profile, ProfileAdmin)

admin.site.unregister(Category)
admin.site.register(Category, CategoryAdmin)

admin.site.unregister(Dataset)
admin.site.register(Dataset, DatasetAdmin)

admin.site.unregister(Service)
admin.site.register(Service, ServiceAdmin)

admin.site.unregister(Cat)
admin.site.register(Cat, CatAdmin)

admin.site.unregister(Product)
admin.site.register(Product, ProductAdmin)

admin.site.unregister(Country)
admin.site.register(Country, CountryAdmin)

admin.site.unregister(StateProvince)
admin.site.register(StateProvince, StateProvinceAdmin)

admin.site.unregister(Address)
admin.site.register(Address, AddressAdmin)

admin.site.unregister(Company)
admin.site.register(Company, CompanyAdmin)

admin.site.unregister(Load)
admin.site.register(Load, LoadAdmin)

admin.site.unregister(Location)
admin.site.register(Location, LocationAdmin)

admin.site.unregister(Device)
admin.site.register(Device, DeviceAdmin)

admin.site.unregister(Stop)
admin.site.register(Stop, StopAdmin)

admin.site.unregister(Route)
admin.site.register(Route, RouteAdmin)

admin.site.unregister(EVChargingLocation)
admin.site.register(EVChargingLocation, EVChargingLocationAdmin)

# TruckType
class TruckTypeAdmin(ModelAdmin):
    list_display = ('name',)
    list_per_page = 100

admin.site.unregister(TruckType)
admin.site.register(TruckType, TruckTypeAdmin)
