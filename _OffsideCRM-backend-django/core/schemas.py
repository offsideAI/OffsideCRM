from .models import Device, Location, Stop, Route, CustomUser, Profile, Load, Address
from datetime import datetime
from ninja import ModelSchema, Schema
from ninja.orm import create_schema
from typing import List, Optional


class UserSchema(Schema):
    class Meta:
        model = CustomUser

    
class LocationSchema(ModelSchema):
    class Meta:
        model = Location
        fields = ('id', 'name', 'slug')
        
    
class DeviceSchema(ModelSchema):
    location: LocationSchema | None = None
    class Meta:
        model = Device
        fields = ('id', 'name', 'slug', 'location')
        
        
class DeviceCreateSchema(Schema):
    name: str
    location_id: int | None = 1
    

class LocationCreateSchema(Schema):
    name: str

class DeviceLocationPatch(Schema):
    location_id: int | None = None


### Error
class Error(Schema):
    message: str
    

### NotFound
class NotFoundSchema(Schema):
    message: str
    
    
 
### StopInput 
class StopInputSchema(Schema):
    title: str
    description: str
    contact_user: Optional[int] = None
    class Meta:
        model = Stop
    

### StopSchema
class StopSchema(ModelSchema):
    class Meta:
        model = Stop
        fields = (
            'id', 
            'title', 
            'description', 
            'origin_address_full', 
            'contact_user'
            )
        
         
### Route

class RouteSchema(Schema):
    id: int
    title: str
    slug: str
    stops: List[StopSchema]
    notes: Optional[str]

class RouteOutputSchema(Schema):
    id: int
    title: str
    slug: str
    route_assigned_to_user: Optional[int] = None
    stops: List[StopSchema]
    notes: Optional[str]

RouteOutputSchema = create_schema(Route, depth=1)

# Or define a Schema class manually if customization is needed
class RouteSchema(Schema):
    id: int
    title: str
    slug: str
    notes: str
    route_assigned_to_user: int | None = None  # Assuming this field stores user ID
    stops: List[StopSchema]  # Define StopSchema as needed

    @staticmethod
    def resolve_route_assigned_to_user(obj):
        return obj.route_assigned_to_user.id if obj.route_assigned_to_user else None

    class Config:
        from_atttributes = True


class ProfileSchema(ModelSchema):
    truck_type: str | None = None

    class Meta:
        model = Profile
        fields = ['capacity', 'license_number', 'phone', 'thumb', 'bio', 'status', 'base_location']

    @staticmethod
    def resolve_truck_type(obj):
        return obj.truck_type.name if obj.truck_type else None


class DriverSchema(ModelSchema):
    profile: ProfileSchema
    date_joined: str | None = None
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email']

    @staticmethod
    def resolve_date_joined(obj):
        return obj.date_joined.isoformat() if obj.date_joined else None


class DriverCreateSchema(Schema):
    first_name: str
    last_name: str
    email: str
    phone: str | None = None
    truck_type: str | None = None
    capacity: int | None = None
    license_number: str | None = None
    status: str = 'active'
    base_location: str | None = None


class DriverUpdateSchema(Schema):
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    phone: str | None = None
    truck_type: str | None = None
    capacity: int | None = None
    license_number: str | None = None
    status: str | None = None
    base_location: str | None = None


class AddressSchema(ModelSchema):
    class Meta:
        model = Address
        fields = ['id', 'address_line1', 'city', 'state_province', 'postal_code', 'country']

class LoadSchema(ModelSchema):
    origin: str | None = None
    destination: str | None = None
    value: float | None = 0.0
    origin_address: AddressSchema | None = None
    dropoff_address: AddressSchema | None = None
    origin_instructions: str | None = None
    destination_instructions: str | None = None

    class Meta:
        model = Load
        fields = [
            'id', 
            'title', 
            'origin_pickup_range_start', 
            'destination_dropoff_range_start', 
            'load_assigned_to_user', 
            'value', 
            'origin_instructions', 
            'destination_instructions'
        ]
    
    @staticmethod
    def resolve_origin(obj):
        if obj.origin_address:
            return f"{obj.origin_address.city}, {obj.origin_address.state_province}"
        return ""

    @staticmethod
    def resolve_destination(obj):
         if obj.dropoff_address:
             return f"{obj.dropoff_address.city}, {obj.dropoff_address.state_province}"
         return ""


class LoadAssignmentSchema(Schema):
    assigned_driver_id: int | None = None

class AddressInputSchema(Schema):
    address_line1: str | None = None
    city: str
    state_province: str
    postal_code: str | None = None
    country: str | None = "USA"

class LoadCreateSchema(Schema):
    title: str
    origin: AddressInputSchema
    destination: AddressInputSchema
    origin_pickup_range_start: datetime
    destination_dropoff_range_start: datetime
    origin_instructions: str | None = None
    destination_instructions: str | None = None
    value: float | None = 0.0
