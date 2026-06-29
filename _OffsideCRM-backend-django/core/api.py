from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from ninja import NinjaAPI
from ninja.openapi.docs import DocsBase
from .authentication import JWTAuth
from .models import Device
from .models import Location
from .models import Stop
from .models import Route
from typing import List, Optional
from .schemas import (
    StopSchema,
    StopInputSchema,
    RouteSchema,
    RouteOutputSchema,
    DeviceSchema,
    LocationSchema,
    DeviceCreateSchema,
    LocationCreateSchema,
    NotFoundSchema,
    Error,
    DeviceLocationPatch,
    DriverSchema,
    DriverCreateSchema,
    DriverUpdateSchema,
    LoadSchema,
    LoadAssignmentSchema,
    LoadCreateSchema,
    AddressInputSchema,
)
from django.contrib.auth.models import User
from .models import Profile, Load
from .models import CustomUser, TruckType
from .models import Profile, Load, BlacklistedAccessToken, Address
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
from ninja import Schema


SWAGGER_DARK_CSS = """
:root {
    --navy-900: #0a1628;
    --navy-800: #0f2140;
    --navy-700: #152d50;
    --navy-600: #1e3a5f;
    --navy-500: #2563eb;
    --text-primary: #e2e8f0;
    --text-secondary: #94a3b8;
    --text-muted: #64748b;
    --accent: #3b82f6;
    --accent-hover: #60a5fa;
    --success: #22c55e;
    --warning: #f59e0b;
    --error: #ef4444;
    --border: #1e3a5f;
}
body { background-color: var(--navy-900) !important; color: var(--text-primary) !important; }
.swagger-ui { color: var(--text-primary); }
.swagger-ui .topbar { background-color: var(--navy-800) !important; border-bottom: 1px solid var(--border); }
.swagger-ui .topbar .download-url-wrapper .select-label select { background: var(--navy-700); color: var(--text-primary); border: 1px solid var(--border); }
.swagger-ui .info { margin: 30px 0; }
.swagger-ui .info .title { color: var(--text-primary) !important; }
.swagger-ui .info .description p, .swagger-ui .info .description { color: var(--text-secondary) !important; }
.swagger-ui .info a { color: var(--accent) !important; }
.swagger-ui .scheme-container { background: var(--navy-800) !important; box-shadow: none !important; border: 1px solid var(--border); border-radius: 8px; padding: 20px !important; }
.swagger-ui .opblock-tag { color: var(--text-primary) !important; border-bottom: 1px solid var(--border) !important; }
.swagger-ui .opblock-tag:hover { background: var(--navy-800) !important; }
.swagger-ui .opblock-tag small { color: var(--text-muted) !important; }
.swagger-ui .opblock { background: var(--navy-800) !important; border: 1px solid var(--border) !important; border-radius: 8px !important; box-shadow: none !important; margin-bottom: 10px; }
.swagger-ui .opblock .opblock-summary { border-bottom: 1px solid var(--border); }
.swagger-ui .opblock .opblock-summary-method { border-radius: 6px !important; font-weight: 600; }
.swagger-ui .opblock.opblock-post { border-color: var(--success) !important; background: rgba(34, 197, 94, 0.05) !important; }
.swagger-ui .opblock.opblock-post .opblock-summary-method { background: var(--success) !important; }
.swagger-ui .opblock.opblock-get { border-color: var(--accent) !important; background: rgba(59, 130, 246, 0.05) !important; }
.swagger-ui .opblock.opblock-get .opblock-summary-method { background: var(--accent) !important; }
.swagger-ui .opblock.opblock-put { border-color: var(--warning) !important; background: rgba(245, 158, 11, 0.05) !important; }
.swagger-ui .opblock.opblock-put .opblock-summary-method { background: var(--warning) !important; }
.swagger-ui .opblock.opblock-delete { border-color: var(--error) !important; background: rgba(239, 68, 68, 0.05) !important; }
.swagger-ui .opblock.opblock-delete .opblock-summary-method { background: var(--error) !important; }
.swagger-ui .opblock .opblock-summary-path, .swagger-ui .opblock .opblock-summary-path__deprecated { color: var(--text-primary) !important; }
.swagger-ui .opblock .opblock-summary-description { color: var(--text-secondary) !important; }
.swagger-ui .opblock .opblock-section-header { background: var(--navy-700) !important; box-shadow: none !important; }
.swagger-ui .opblock .opblock-section-header h4 { color: var(--text-primary) !important; }
.swagger-ui .opblock-body pre { background: var(--navy-900) !important; color: var(--text-primary) !important; border: 1px solid var(--border); border-radius: 6px; }
.swagger-ui .opblock-description-wrapper p, .swagger-ui .opblock-external-docs-wrapper p { color: var(--text-secondary) !important; }
.swagger-ui table thead tr th, .swagger-ui table thead tr td { color: var(--text-primary) !important; border-bottom: 1px solid var(--border) !important; }
.swagger-ui table tbody tr td { color: var(--text-secondary) !important; border-bottom: 1px solid var(--border) !important; }
.swagger-ui .parameter__name { color: var(--text-primary) !important; }
.swagger-ui .parameter__type { color: var(--accent) !important; }
.swagger-ui .parameter__in { color: var(--text-muted) !important; }
.swagger-ui input[type=text], .swagger-ui input[type=password], .swagger-ui input[type=email], .swagger-ui textarea, .swagger-ui select { background: var(--navy-700) !important; color: var(--text-primary) !important; border: 1px solid var(--border) !important; border-radius: 6px !important; }
.swagger-ui input[type=text]:focus, .swagger-ui input[type=password]:focus, .swagger-ui textarea:focus { border-color: var(--accent) !important; outline: none !important; }
.swagger-ui .btn { border-radius: 6px !important; font-weight: 500; }
.swagger-ui .btn.execute { background-color: var(--accent) !important; border-color: var(--accent) !important; }
.swagger-ui .btn.execute:hover { background-color: var(--accent-hover) !important; }
.swagger-ui .btn.authorize { background-color: var(--success) !important; border-color: var(--success) !important; color: white !important; }
.swagger-ui .btn.cancel { background-color: var(--navy-600) !important; border-color: var(--border) !important; }
.swagger-ui .model-box { background: var(--navy-800) !important; border-radius: 8px; }
.swagger-ui .model { color: var(--text-primary) !important; }
.swagger-ui .model-title { color: var(--text-primary) !important; }
.swagger-ui .prop-type { color: var(--accent) !important; }
.swagger-ui .prop-format { color: var(--text-muted) !important; }
.swagger-ui section.models { border: 1px solid var(--border) !important; border-radius: 8px; }
.swagger-ui section.models.is-open h4 { border-bottom: 1px solid var(--border) !important; }
.swagger-ui section.models h4 { color: var(--text-primary) !important; }
.swagger-ui .model-container { background: var(--navy-800) !important; border-radius: 6px; margin: 10px 0; }
.swagger-ui .responses-inner h4, .swagger-ui .responses-inner h5 { color: var(--text-primary) !important; }
.swagger-ui .response-col_status { color: var(--text-primary) !important; }
.swagger-ui .response-col_description__inner p { color: var(--text-secondary) !important; }
.swagger-ui .responses-table thead td { color: var(--text-primary) !important; }
.swagger-ui .loading-container .loading:after { color: var(--accent) !important; }
.swagger-ui .dialog-ux .modal-ux { background: var(--navy-800) !important; border: 1px solid var(--border) !important; border-radius: 12px !important; }
.swagger-ui .dialog-ux .modal-ux-header { border-bottom: 1px solid var(--border) !important; }
.swagger-ui .dialog-ux .modal-ux-header h3 { color: var(--text-primary) !important; }
.swagger-ui .dialog-ux .modal-ux-content p { color: var(--text-secondary) !important; }
.swagger-ui .dialog-ux .modal-ux-content h4 { color: var(--text-primary) !important; }
.swagger-ui .auth-container { border-color: var(--border) !important; }
.swagger-ui .auth-container h4 { color: var(--text-primary) !important; }
.swagger-ui .auth-container .wrapper { border-color: var(--border) !important; }
.swagger-ui .scopes h2 { color: var(--text-primary) !important; }
.swagger-ui .checkbox p { color: var(--text-secondary) !important; }
.swagger-ui .markdown p, .swagger-ui .markdown pre, .swagger-ui .renderedMarkdown p { color: var(--text-secondary) !important; }
.swagger-ui .markdown code, .swagger-ui .renderedMarkdown code { background: var(--navy-700) !important; color: var(--accent) !important; padding: 2px 6px; border-radius: 4px; }
.swagger-ui ::-webkit-scrollbar { width: 8px; height: 8px; }
.swagger-ui ::-webkit-scrollbar-track { background: var(--navy-800); border-radius: 4px; }
.swagger-ui ::-webkit-scrollbar-thumb { background: var(--navy-600); border-radius: 4px; }
.swagger-ui ::-webkit-scrollbar-thumb:hover { background: var(--navy-500); }
.swagger-ui .highlight-code .hljs { background: var(--navy-900) !important; color: var(--text-primary) !important; }
.swagger-ui .microlight { background: var(--navy-900) !important; color: var(--text-primary) !important; }
"""


class DarkSwaggerDocs(DocsBase):
    def render_page(self, request, api, **kwargs):
        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>FR8 Pro API</title>
    <link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui.css">
    <style>{SWAGGER_DARK_CSS}</style>
</head>
<body>
    <div id="swagger-ui"></div>
    <script src="https://cdn.jsdelivr.net/npm/swagger-ui-dist@5/swagger-ui-bundle.js"></script>
    <script>
        window.onload = function() {{
            SwaggerUIBundle({{
                url: "{api.root_path}/openapi.json",
                dom_id: '#swagger-ui',
                presets: [
                    SwaggerUIBundle.presets.apis,
                    SwaggerUIBundle.SwaggerUIStandalonePreset
                ],
                layout: "BaseLayout",
                persistAuthorization: true,
                docExpansion: "list"
            }});
        }};
    </script>
</body>
</html>"""
        return HttpResponse(html)


api = NinjaAPI(csrf=False, docs=DarkSwaggerDocs())

class LogoutSchema(Schema):
    refresh: str

@api.post('auth/logout', auth=JWTAuth())
def logout(request, data: LogoutSchema):
    """
    Unified Logout: Invalidates BOTH Access Token and Refresh Token.
    1. Blacklists Access Token (from Authorization Header)
    2. Blacklists Refresh Token (from Request Body)
    """
    # 1. Blacklist Access Token
    auth_header = request.headers.get("Authorization")
    if auth_header:
        token_str = None
        if auth_header.startswith("Bearer "):
            token_str = auth_header.split(" ")[1]
        elif auth_header.startswith("JWT "):
            token_str = auth_header.split(" ")[1]
            
        if token_str:
            try:
               jwt_auth = JWTAuthentication()
               validated_token = jwt_auth.get_validated_token(token_str)
               jti = validated_token.get('jti')
               
               if not BlacklistedAccessToken.objects.filter(token_jti=jti).exists():
                   BlacklistedAccessToken.objects.create(token_jti=jti, user=request.auth)
            except Exception:
               pass

    # 2. Blacklist Refresh Token
    try:
        token = RefreshToken(data.refresh)
        token.blacklist()
    except TokenError:
        return 400, {"message": "Invalid refresh token"}

    return 200, {"message": "Logged out successfully"}

# ==========================================
# Stops API
# ==========================================

@api.get('stops/', response=List[StopSchema], auth=JWTAuth())
def get_stops(request):
    """
    Retrieve all stops.
    """
    return Stop.objects.all()

@api.get('stops/{stop_id}', response={200: StopSchema, 404: NotFoundSchema})
def get_stop(request, stop_id: int):
    """
    Retrieve a specific stop by its ID.
    """
    try:
        stop = Stop.objects.get(pk=stop_id)
        return 200, stop
    except Stop.DoesNotExist:
        return 404, {"message": "Stop does not exist"}

@api.get('stops', response=List[StopSchema], auth=JWTAuth())
def get_stops_by_contact(request, contact_user: Optional[int] = None):
    """
    Retrieve stops, optionally filtered by the assigned contact user.
    """
    if contact_user:
        return Stop.objects.filter(contact_user=contact_user)
    return Stop.objects.all()

@api.post('stops/', response={201: StopSchema})
def create_stop(request, stop: StopInputSchema):
    """
    Create a new stop.
    """
    # Validate user existence
    user_id = stop.contact_user 
    if user_id is not None:
        contact_user = get_object_or_404(CustomUser, id=user_id)
    else:
        contact_user = None
    
    stop_data = stop.dict(exclude={'contact_user'}) 
    stop_model = Stop.objects.create(contact_user=contact_user, **stop_data)
    return stop_model

@api.put('stops/{stop_id}', response={200: StopSchema, 404: NotFoundSchema})
def update_stop(request, stop_id: int, data: StopInputSchema):
    """
    Update an existing stop.
    """
    try:
        stop = Stop.objects.get(pk=stop_id)
        # Handle updating contact_user separately if it's in the payload
        user_id = data.dict().pop('contact_user', None)
        if user_id is not None:
            contact_user = get_object_or_404(CustomUser, id=user_id)
            stop.contact_user = contact_user

        # Update other attributes
        for attribute, value in data.dict(exclude={'contact_user'}).items():
            setattr(stop, attribute, value)

        stop.save()
        return 200, stop
    
    except Stop.DoesNotExist:
         return 404, {"message": "Stop does not exist"} 

@api.delete('stops/{stop_id}', response={200: None, 404: NotFoundSchema})
def delete_stop(request, stop_id: int, data: StopInputSchema):
    """
    Delete a stop.
    """
    try:
       stop = Stop.objects.get(pk=stop_id)
       stop.delete()
       return 200
    except Stop.DoesNotExist:
         return 404, {"message": "Stop does not exist"} 

# ==========================================
# Routes API
# ==========================================

@api.get('routes/', response=List[RouteOutputSchema], auth=JWTAuth())
def get_routes(request):
    """
    Retrieve all routes with manual serialization for related fields.
    """
    routes = Route.objects.all()
    # Process each route to manually handle foreign key serialization
    processed_routes = []
    for route in routes:
        route_data = {
            "id": route.id,
            "title": route.title,
            "slug": route.slug,
            "stops": route.stops.all(),  # Assuming stops is a many-to-many field
            "notes": route.notes,
            # Extract the user ID explicitly if route_assigned_to_user is not None
            "route_assigned_to_user": route.route_assigned_to_user.id if route.route_assigned_to_user else None,
        }
        processed_routes.append(route_data)
    return processed_routes

@api.get('routes/{route_id}', response={200: RouteOutputSchema, 404: NotFoundSchema})
def get_routes_by_id(request, route_id: int):
    """
    Retrieve a specific route by its ID.
    """
    try:
        route = Route.objects.get(pk=route_id)
        return 200, route
    except Route.DoesNotExist:
        return 404, {"message": "Route does not exist"}

@api.get('routes', response=List[RouteOutputSchema], auth=JWTAuth())
def get_routes_filtered_by_route_assigned_to_user(request, route_assigned_to_user: Optional[int] = None):
    """
    Retrieve routes, optionally filtered by the assigned user.
    """
    queryset = Route.objects.all()

    if route_assigned_to_user:
        queryset = queryset.filter(route_assigned_to_user=route_assigned_to_user)

    processed_routes = []
    for route in queryset:
        stops = list(route.stops.all().order_by('ordering_number'))
        route_data = {
            "id": route.id,
            "title": route.title,
            "slug": route.slug,
            "stops": stops,  # Serialize or transform `stops` as needed for your response schema
            "notes": route.notes,
            # Simplify `route_assigned_to_user` to include only necessary fields
            "route_assigned_to_user_id": route.route_assigned_to_user.id if route.route_assigned_to_user else None,
        }
        processed_routes.append(route_data)

    return processed_routes

# ==========================================
# Devices API
# ==========================================

@api.get('devices/', response=list[DeviceSchema], auth=JWTAuth())
def get_devices(request):
    """
    Retrieve all devices.
    """
    return Device.objects.all()


@api.get('devices/{slug}/', response=DeviceSchema)
def get_device(request, slug: str):
    """
    Retrieve a specific device by its slug.
    """
    device = get_object_or_404(Device, slug=slug)
    return device


@api.post('devices/', response={200: DeviceSchema, 404: Error})
def create_device(request, device: DeviceCreateSchema):
    """
    Create a new device.
    """
    if device.location_id:
        # we have a location ID in the body
        location_exists = Location.objects.filter(id=device.location_id).exists()
        if not location_exists:
            return 404, {"message": "Location not found"}
    device_data = device.model_dump()
    device_model = Device.objects.create(**device_data)
    return device_model

@api.post('devices/{device_slug}/set-location/', response=DeviceSchema)
def update_device_location(request, device_slug, location: DeviceLocationPatch):
    """
    Update the location of a specific device.
    """
    device = get_object_or_404(Device, slug=device_slug)
    if location.location_id:
        location = get_object_or_404(Location, id=location.location_id)
        device.location = location
    else:
        device.location = None
        
    device.save()
    return device

# ==========================================
# Locations API
# ==========================================

@api.get('locations/', response=list[LocationSchema])
def get_locations(request):
    """
    Retrieve all locations.
    """
    return Location.objects.all()

@api.post('locations/', response={200: LocationSchema, 404: Error})
def create_location(request, location: LocationCreateSchema):
    """
    Create a new location.
    """
    location_data = location.dict()
    location_model = Location.objects.create(**location_data)
    return location_model

# ==========================================
# Drivers API
# ==========================================

@api.get('drivers/', response=List[DriverSchema], auth=JWTAuth())
def get_drivers(request):
    """
    Retrieve all drivers scoped to the authenticated user's company.
    A driver is a user whose Profile has a truck_type set.
    """
    user_profile, _ = Profile.objects.get_or_create(user=request.auth)
    if not user_profile.company:
        return []
    return CustomUser.objects.select_related('profile', 'profile__truck_type').filter(
        profile__truck_type__isnull=False,
        profile__company=user_profile.company,
    )


@api.post('drivers/', response={200: DriverSchema, 403: Error}, auth=JWTAuth())
def create_driver(request, data: DriverCreateSchema):
    """
    Create a new driver (CustomUser + Profile) within the authenticated user's company.
    """
    user_profile, _ = Profile.objects.get_or_create(user=request.auth)
    if not user_profile.company:
        return 403, {"message": "User must belong to a company"}

    # Create the CustomUser
    new_user = CustomUser.objects.create_user(
        username=data.email,
        email=data.email,
        first_name=data.first_name,
        last_name=data.last_name,
        password=CustomUser.objects.make_random_password(),
    )

    # Create or update the Profile with driver fields
    profile, _ = Profile.objects.get_or_create(user=new_user)
    profile.company = user_profile.company
    truck_type_name = data.truck_type or 'Semi'
    profile.truck_type, _ = TruckType.objects.get_or_create(name=truck_type_name)
    profile.capacity = data.capacity
    profile.license_number = data.license_number
    profile.phone = data.phone
    profile.status = data.status
    profile.base_location = data.base_location
    profile.save()

    return new_user


@api.put('drivers/{driver_id}/', response={200: DriverSchema, 403: Error, 404: Error}, auth=JWTAuth())
def update_driver(request, driver_id: int, data: DriverUpdateSchema):
    """
    Update an existing driver's user and profile fields.
    """
    user_profile, _ = Profile.objects.get_or_create(user=request.auth)
    if not user_profile.company:
        return 403, {"message": "User must belong to a company"}

    driver = get_object_or_404(CustomUser, id=driver_id)
    driver_profile, _ = Profile.objects.get_or_create(user=driver)

    if driver_profile.company != user_profile.company:
        return 403, {"message": "You do not have permission to edit this driver"}

    # Update user fields
    if data.first_name is not None:
        driver.first_name = data.first_name
    if data.last_name is not None:
        driver.last_name = data.last_name
    if data.email is not None:
        driver.email = data.email
        driver.username = data.email
    driver.save()

    # Update profile fields
    if data.truck_type is not None:
        driver_profile.truck_type, _ = TruckType.objects.get_or_create(name=data.truck_type)
    if data.capacity is not None:
        driver_profile.capacity = data.capacity
    if data.license_number is not None:
        driver_profile.license_number = data.license_number
    if data.phone is not None:
        driver_profile.phone = data.phone
    if data.status is not None:
        driver_profile.status = data.status
    if data.base_location is not None:
        driver_profile.base_location = data.base_location
    driver_profile.save()

    return driver


@api.delete('drivers/{driver_id}/', response={200: None, 403: Error}, auth=JWTAuth())
def delete_driver(request, driver_id: int):
    """
    Delete a driver. Only allowed within the same company.
    """
    user_profile, _ = Profile.objects.get_or_create(user=request.auth)
    if not user_profile.company:
        return 403, {"message": "User must belong to a company"}

    driver = get_object_or_404(CustomUser, id=driver_id)
    driver_profile, _ = Profile.objects.get_or_create(user=driver)

    if driver_profile.company != user_profile.company:
        return 403, {"message": "You do not have permission to delete this driver"}

    driver.delete()
    return 200


# ==========================================
# Loads API
# ==========================================

from django.db.models import Q

@api.get('loads/', response=List[LoadSchema], auth=JWTAuth())
def get_loads(request):
    """
    Retrieve all loads, filtered by the authenticated user's company.
    If the user has no company, returns an empty list (or could 403).
    """
    user_profile, created = Profile.objects.get_or_create(user=request.auth)
    if not user_profile.company:
        return []
        
    return Load.objects.filter(
        Q(origin_company=user_profile.company) | 
        Q(destination_company=user_profile.company)
    )


@api.patch('loads/{load_id}/', response=LoadSchema, auth=JWTAuth())
def assign_driver(request, load_id: int, data: LoadAssignmentSchema):
    """
    Assign or unassign a driver to/from a specific load.
    Send assigned_driver_id: null to unassign (resets to the requesting user).
    """
    load = get_object_or_404(Load, id=load_id)
    if data.assigned_driver_id is None:
        load.load_assigned_to_user = request.auth
    else:
        driver = get_object_or_404(CustomUser, id=data.assigned_driver_id)
        load.load_assigned_to_user = driver
    load.save()
    return load

@api.post('loads/', response={200: LoadSchema, 403: Error}, auth=JWTAuth())
def create_load(request, data: LoadCreateSchema):
    user_profile, created = Profile.objects.get_or_create(user=request.auth)
    if not user_profile.company:
         return 403, {"message": "User must belong to a company"}
    
    # Process origin address data to handle Country ForeignKey
    origin_data = data.origin.dict()
    origin_country = origin_data.pop('country', None)
    if origin_country:
        origin_data['country_id'] = origin_country
    origin_addr = Address.objects.create(**origin_data)

    # Process destination address data to handle Country ForeignKey
    dest_data = data.destination.dict()
    dest_country = dest_data.pop('country', None)
    if dest_country:
        dest_data['country_id'] = dest_country
    dest_addr = Address.objects.create(**dest_data)
         
    load = Load.objects.create(
        title=data.title,
        origin_address=origin_addr,
        dropoff_address=dest_addr,
        origin_pickup_range_start=data.origin_pickup_range_start,
        destination_dropoff_range_start=data.destination_dropoff_range_start,
        value=data.value,
        origin_company=user_profile.company, 
        destination_company=user_profile.company,
        origin_instructions=data.origin_instructions,
        destination_instructions=data.destination_instructions,
        number_of_skids=0 
    )
    return load

@api.put('loads/{load_id}/', response={200: LoadSchema, 403: Error}, auth=JWTAuth())
def update_load(request, load_id: int, data: LoadCreateSchema):
    load = get_object_or_404(Load, id=load_id)
    user_profile, created = Profile.objects.get_or_create(user=request.auth)
    
    if load.origin_company != user_profile.company and load.destination_company != user_profile.company:
        return 403, {"message": "You do not have permission to edit this load"}
    
    if load.origin_address:
         origin_updates = data.origin.dict()
         country_code = origin_updates.pop('country', None)
         if country_code:
             load.origin_address.country_id = country_code
             
         for attr, value in origin_updates.items():
             setattr(load.origin_address, attr, value)
         load.origin_address.save()
    else:
         origin_data = data.origin.dict()
         country_code = origin_data.pop('country', None)
         if country_code:
             origin_data['country_id'] = country_code
         load.origin_address = Address.objects.create(**origin_data)

    if load.dropoff_address:
         dest_updates = data.destination.dict()
         country_code = dest_updates.pop('country', None)
         if country_code:
             load.dropoff_address.country_id = country_code

         for attr, value in dest_updates.items():
             setattr(load.dropoff_address, attr, value)
         load.dropoff_address.save()
    else:
         dest_data = data.destination.dict()
         country_code = dest_data.pop('country', None)
         if country_code:
             dest_data['country_id'] = country_code
         load.dropoff_address = Address.objects.create(**dest_data)
    
    load.title = data.title
    load.origin_pickup_range_start = data.origin_pickup_range_start
    load.destination_dropoff_range_start = data.destination_dropoff_range_start
    load.value = data.value
    load.origin_instructions = data.origin_instructions
    load.destination_instructions = data.destination_instructions
    load.save()
    return load

@api.delete('loads/{load_id}/', response={200: None, 403: Error}, auth=JWTAuth())
def delete_load(request, load_id: int):
     load = get_object_or_404(Load, id=load_id)
     user_profile, created = Profile.objects.get_or_create(user=request.auth)
     if load.origin_company != user_profile.company and load.destination_company != user_profile.company:
        return 403, {"message": "You do not have permission to delete this load"}
     load.delete()
     return 200
