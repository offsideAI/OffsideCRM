from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from io import BytesIO
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile
import uuid
from django.utils import timezone
# from pytz import timezone
from dateutil.tz import tzlocal
from datetime import datetime
from django.utils.timezone import now
from django.utils.safestring import mark_safe
from django.conf import settings
from django.core.files import File
from io import BytesIO
from PIL import Image
from django_extensions.db.fields import AutoSlugField
from django.contrib.postgres.fields import ArrayField

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_deactivated = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return str(self.email)
    

# TruckType
class TruckType(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name_plural = "truck types"
        ordering = ['name']

    def __str__(self):
        return self.name


# Profile
class Profile(models.Model):
    DEFAULT_PK=1
    REGULAR = 1
    ADMIN = 2
    GOD = 3
    ROLE_CHOICES = (
        (REGULAR, 'regular'),
        (ADMIN, 'admin'),
        (GOD, 'god'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    isactive = models.BooleanField(default=False)
    userid = models.UUIDField(default=uuid.uuid4)
    bio = models.TextField(max_length=500, blank=True)
    birthdate = models.DateField(null=True, blank=True)
    handle = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICES, null=True, blank=True)
    
    # Company Link
    company = models.ForeignKey('Company', on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    
    # Driver Fields
    truck_type = models.ForeignKey(TruckType, on_delete=models.SET_NULL, null=True, blank=True)
    capacity = models.IntegerField(blank=True, null=True)
    license_number = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    thumb = models.ImageField(default='default.png', upload_to='uploads/', blank=True, null=True)

    DRIVER_STATUS_CHOICES = [
        ('active', 'Active'),
        ('rest', 'Rest'),
        ('off_duty', 'Off Duty'),
    ]
    status = models.CharField(max_length=10, choices=DRIVER_STATUS_CHOICES, default='active', blank=True)
    base_location = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name_plural = "profiles"
    def __str__(self):
        return str(self.id)

    def thumb_tag(self):
        if self.thumb:
            return mark_safe('<img src="%s" style="width: 568px; height:320px;" />' % self.thumb.url)
        else:
            return 'No Image Found'
        thumb_tag.short_description = 'Thumb'
        
        
# PropertyType
class PropertyType(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "propertytypes"
    
    def __str__(self):
        return self.name
    
# PropertyStatus
class PropertyStatus(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    class Meta:
        verbose_name_plural = "propertystatus"
    
    def __str__(self):
        return self.name
    

# Property
class Property(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    slug = models.SlugField(blank=True)
    description = models.TextField()
    fulladdress = models.TextField()
    streetAddressLineOne = models.CharField(max_length=400)
    streetAddressLineTwo = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    latitude = models.CharField(max_length=200)
    longitude = models.CharField(max_length=200)
    zpid = models.CharField(max_length=200)
    livingArea = models.CharField(max_length=200)
    bathrooms = models.CharField(max_length=200)
    bedrooms = models.CharField(max_length=200)
    askingPrice = models.CharField(max_length=200)
    propzPrice = models.CharField(max_length=200)
    rentalMonthly = models.CharField(max_length=200)
    propertyType = models.ForeignKey(PropertyType, on_delete=models.CASCADE, default=PropertyType.DEFAULT_PK)
    propertyStatus = models.ForeignKey(PropertyStatus, on_delete=models.CASCADE, default=PropertyStatus.DEFAULT_PK)
    image = models.ImageField(upload_to='media/', blank=True)
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='property_created_user')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    date_published = models.DateTimeField(auto_now_add=True)
    isfavorite = models.BooleanField(default=False)
    isfeatured = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "properties"
    
    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Open the uploaded image
        im = Image.open(self.image)
        output = BytesIO()
        original_width, original_height = im.size
        aspect_ratio = round(original_width / original_height)
        desired_width = 250
        desired_height = desired_width * aspect_ratio
        # Resize the image
        im = im.resize((desired_width, desired_height))
        # after modifications, save it to the output
        im.save(output, format='PNG', quality=90)
        output.seek(0)
        # change the imagefield value to be the newly modifed image value
        self.image = InMemoryUploadedFile(output, 'ImageField', "%s.png" % self.image.name.split('.')[0], 'image/png',
                                    sys.getsizeof(output), None)
        super(Property, self).save(*args, **kwargs)

    def image_tag(self):
        if self.image:
            return mark_safe('<img src="%s" style="width: 284px; height:160px;" />' % self.image.url)
        else:
            return 'No Image Found'

# Category
# Product is to Cat as Service is to Category

class Category(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        ordering = ('-created_at', '-id')
        verbose_name_plural = 'categories'
        
    def __str__(self):
        return self.name
    
    

# Cat
# Product is to Cat as Service is to Category
class Cat(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta: 
        ordering = ('-created_at', '-id')
        verbose_name_plural = 'cats'
        
    def __str__(self):
        return self.name

# Dataset
class Dataset(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='dataset_created_user')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    
    class Meta: 
        ordering = ('-created_at', '-id')
        
    def __str__(self):
        return self.name
    
    def get_display_price(self): 
        return self.price / 100
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image: 
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
            
    def make_thumbnail(self, image, size=(300,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
        

# Service
class Service(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    category = models.ForeignKey(Category, related_name='services', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='service_created_user')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    
    class Meta: 
        ordering = ('-created_at', '-id')
        
    def __str__(self):
        return self.name
    
    def get_display_price(self): 
        return self.price / 100
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image: 
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
            
    def make_thumbnail(self, image, size=(300,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
        
        
# Product
class Product(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    cat = models.ForeignKey(Cat, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField(blank=True, null=True)
    price = models.IntegerField()
    created_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='product_created_user')
    created_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    
    class Meta: 
        ordering = ('-created_at', '-id')
        
    def __str__(self):
        return self.name
    
    def get_display_price(self): 
        return self.price / 100
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image: 
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg'
            
    def make_thumbnail(self, image, size=(300,300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)
        return thumbnail
    
    def get_fields(self):
        return [(field.verbose_name, field.value_from_object(self))
            
            if field.verbose_name != 'cat' 
            
            else 
                (field.verbose_name, 
                Cat.objects.get(pk=field.value_from_object(self)).name)
            
            for field in self.__class__._meta.fields[1:]
        ]
    
   
# Country
class Country(models.Model):
    """Model for countries"""
    iso_code = models.CharField(max_length = 3, primary_key = True)
    name = models.CharField(max_length = 45, blank = False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Countries"
        ordering = ["name", "iso_code"]

# StateProvince
class StateProvince(models.Model):
    """Model for states and provinces"""
    iso_code = models.CharField(max_length = 3, primary_key = True)
    name = models.CharField(max_length = 55, blank = False)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, to_field="iso_code")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "State or province"
        verbose_name_plural = "stateprovinces"
        """the admin site dies when I try this. apparantely support for
           ordering by foreign keys is broken. uncomment when fixed
           ordering = ["-country", "name"]
        """
         
# Address
class Address(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    """Model to store addresses for accounts"""
    address_line1 = models.CharField("Address line 1", max_length = 45, blank = True)
    address_line2 = models.CharField("Address line 2", max_length = 45, blank = True)
    postal_code = models.CharField("Postal Code", max_length = 10, blank = True)
    city = models.CharField(max_length = 50, blank = True)
    state_province = models.CharField("State/Province", max_length = 40, blank = True)
    state_or_province = models.ForeignKey(StateProvince, on_delete=models.SET_NULL, null = True, blank = True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank = True)
    address_notes = models.CharField(max_length=200, blank = True)
    address_lat = models.CharField("Address lat", max_length = 45, null=True, blank = True)
    address_lng = models.CharField("Address lng", max_length = 45, null=True, blank = True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null = True, blank = True, related_name='address_linked_user')
    def __str__(self):
        return "%s, %s, %s, %s %s" % (self.address_line1, self.address_line2, self.city, self.state_province,
                              str(self.country))

    class Meta:
        verbose_name_plural = "addresses"
        unique_together = ("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")


    
 
# Company
class Company(models.Model):
    DEFAULT_PK=0
    OWNER_OPERATOR = 1
    CARRIER = 2
    DRIVER = 3
    SHIPPER = 4
    MERCHANT = 5
    VENDOR = 6
    COMPANY_TYPE_CHOICES = (
        (OWNER_OPERATOR, 'owner_operator'),
        (CARRIER, 'carrier'),
        (DRIVER, 'driver'),
        (SHIPPER, 'shipper'),
        (MERCHANT, 'merchant'),
        (VENDOR, 'vendor'),
    )
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    desc = models.CharField(max_length=200)
    isfeatured = models.BooleanField(default=False)
    isprivatelabel = models.BooleanField(default=False)
    isactive = models.BooleanField(default=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, null=True, blank=True)
    address = models.ForeignKey(Address, on_delete=models.SET_NULL, default=Address.DEFAULT_PK, null=True, blank=True)
    company_type = models.PositiveSmallIntegerField(choices=COMPANY_TYPE_CHOICES, null=True, blank=True)
    upvotes = models.IntegerField(default=0, null=True, blank=True)
    downvotes = models.IntegerField(default=0, null=True, blank=True)
    cell_phone = models.CharField(max_length=200)
    work_phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    website_url = models.CharField(max_length=200)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    class Meta:
        verbose_name_plural = "companies"
    
    def __str__(self):
        return self.name

    def thumb_tag(self):
        if self.thumb:
            return mark_safe('<img src="%s" style="width: 568px; height:320px;" />' % self.thumb.url)
        else:
            return 'No Image Found'
        thumb_tag.short_description = 'Thumb' 
        
        
# Load
class Load(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    origin_tracking_number = models.CharField(max_length=200, blank=True, null=True)
    load_number = models.CharField(max_length=200, blank=True, null=True)
    manifest_number = models.CharField(max_length=200, blank=True, null=True)
    destination_tracking_number = models.CharField(max_length=200, blank=True, null=True)
    title = models.CharField(max_length=200, blank=True, null=True)
    desc = models.CharField(max_length=200, blank=True, null=True)
    origin_places_id = models.CharField(max_length=200, blank=True, null=True)
    destination_places_id = models.CharField(max_length=200, blank=True, null=True)
    origin_address = models.ForeignKey(Address, on_delete=models.PROTECT, default=Address.DEFAULT_PK, null=True, blank=True, related_name='from_address')
    dropoff_address = models.ForeignKey(Address, on_delete=models.PROTECT, default=Address.DEFAULT_PK, null=True, blank=True, related_name='to_address')
    origin_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)  
    origin_lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)  
    destination_lat = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)  
    destination_lng = models.DecimalField(max_digits=22, decimal_places=16, blank=True, null=True)  
    origin_company = models.ForeignKey(Company, on_delete=models.PROTECT, default=Company.DEFAULT_PK, null=True, blank=True, related_name='load_from_company')
    destination_company = models.ForeignKey(Company, on_delete=models.PROTECT, default=Company.DEFAULT_PK, null=True, blank=True, related_name='load_to_company')
    number_of_skids = models.IntegerField()
    origin_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='load_user_origin')
    destination_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='load_user_destination')
    origin_pickup_range_start = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    origin_pickup_range_end = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    destination_dropoff_range_start = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    destination_dropoff_range_end = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    origin_instructions=models.CharField(max_length=200, blank=True, null=True)
    destination_instructions=models.CharField(max_length=200, blank=True, null=True)
    origin_is_appointment = models.BooleanField(default=False)
    destination_is_appointment = models.BooleanField(default=False)
    load_created_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='load_created_by_user')
    load_assigned_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='load_assigned_to_user')
    load_assigned_by_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=Profile.DEFAULT_PK, related_name='load_assigned_by_user')
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)
    proof_of_pickup_picture_1 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_pickup_picture_2 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_pickup_picture_3 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_pickup_picture_4 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_pickup_picture_5 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_delivery_picture_1 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_delivery_picture_2 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_delivery_picture_3 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_delivery_picture_4 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_delivery_picture_5 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    load_assigned_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    load_started_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    load_completion_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_test_data = models.BooleanField(default=True)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, blank=True, null=True)

    
    class Meta:
        verbose_name_plural = "loads"
    
    def __str__(self):
        return f"{self.title} - {self.id}"
    
    def thumb_tag(self):
        if self.thumb:
            return mark_safe('<img src="%s" style="width: 568px; height:320px;" />' % self.thumb.url)
        else:
            return 'No Image Found'
        thumb_tag.short_description = 'Thumb'
        
# Location
class Location(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')
    address_line1 = models.CharField("Address line 1", max_length = 45, blank = True, null=True)
    address_line2 = models.CharField("Address line 2", max_length = 45, blank = True, null=True)
    postal_code = models.CharField("Postal Code", max_length = 10, blank = True, null=True)
    city = models.CharField(max_length = 50, blank = True)
    state_province = models.CharField("State/Province", max_length = 40, blank = True, null=True)
    state_or_province = models.ForeignKey(StateProvince, on_delete=models.PROTECT, blank = True, null=True)
    country = models.ForeignKey(Country, on_delete=models.PROTECT, blank = True, null=True)
    address_notes = models.CharField(max_length=200, blank = True)
    address_lat = models.CharField("Address lat", max_length = 45, blank = True, null=True)
    address_lng = models.CharField("Address lng", max_length = 45, blank = True, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, default=1, related_name='location_linked_user')
    
    def __str__(self):
        return "%s, %s, %s, %s %s" % (self.address_line1, self.address_line2, self.city, self.state_province,
                              str(self.country))

    class Meta:
        verbose_name_plural = "locations"
        unique_together = ("address_line1", "address_line2", "postal_code",
                           "city", "state_province", "country")

    
    def __str__(self):
        return self.name

# Device
class Device(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='name')
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = "devices"
    
    def __str__(self):
        return f"{self.name} - {self.id}"
    
    
# Stop
class Stop(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    description = models.CharField(max_length=200)
    origin_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='stop_origin_address')
    origin_address_full = models.CharField(max_length=255, blank=True, null=True)
    origin_window_range_start = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    origin_notes = models.CharField(max_length=200, blank=True, null=True)
    destination_address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True, related_name='stop_destination_address')
    destination_address_full = models.CharField(max_length=255, blank=True, null=True)
    destination_window_range_start = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    destination_notes = models.CharField(max_length=200, blank=True, null=True)
    ordering_number = models.IntegerField(default=0, null=True, blank=True)
    origin_tracking_number = models.CharField(max_length=200, blank=True, null=True)
    load_number = models.CharField(max_length=200, blank=True, null=True)
    manifest_number = models.CharField(max_length=200, blank=True, null=True)
    destination_tracking_number = models.CharField(max_length=200, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_pickup_picture_1 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    proof_of_delivery_picture_1 = models.ImageField(upload_to='uploads/', blank=True, null=True)
    contact_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='stop_contact_user', null=True, blank=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    
    class Meta:
        verbose_name_plural = "stops"

    def __str__(self):
        return f"{self.title} - {self.id}"


# Route
class Route(models.Model):
    DEFAULT_PK=0
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=200)
    slug = AutoSlugField(populate_from='title')
    stops = models.ManyToManyField(Stop, blank=True, default=[0], related_name='stops_in_this_route')
    route_assigned_to_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='route_assigned_to_user', null=True, blank=True)
    notes = models.CharField(max_length=200, blank=True, null=True)
    
    
    class Meta:
        verbose_name_plural = "routes"
        
    def __str__(self):
        return f"{self.title} - {self.id}"
    
    
# EVChargingLocation
class EVChargingLocation(models.Model):
    station_name = models.CharField(max_length=250)
    station_address = models.CharField(max_length=250)
    latitude = models.FloatField()
    longitude = models.FloatField()
    
    class Meta:
        verbose_name_plural = "evcharginglocations"

    def __str__(self):
        return self.station_name

class BlacklistedAccessToken(models.Model):
    token_jti = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Blacklisted JTI: {self.token_jti}"
