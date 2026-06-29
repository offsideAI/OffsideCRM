from django.contrib.auth import login, authenticate, logout
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Product
# from .models import User
from django.contrib.auth import get_user_model
from django.contrib import messages #import messages
from django.http import JsonResponse
from django.conf import settings

from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, AddProductForm
from .forms import AddCompanyForm
from .models import Company

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer

from djoser.views import UserViewSet
import folium 
from core.models import EVChargingLocation

from django.views.generic.edit import CreateView
from .models import Stop
# Class Based Views (CBV)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
# CBV Product
from .models import Product


# Create your views here.

def frontpage(request):
    # products = Product.objects.all()[0:20]
    # return render(request, 'core/frontpage.html', {'products': products})
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('/dashboard/')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error"))
            return redirect('login')
    else:
        return render(request, 'core/frontpage.html', {})

def dashboard(request):
    products = Product.objects.all()
    stations = EVChargingLocation.objects.all()
    
    # create a Foliummmmm map centered
    m = folium.Map(location=[47.4076457, -78.319689], zoom_start=9)
    
    map = folium.Map(location=[45.5074447, -73.5545917], # lat and lon of the starting point
                 width="100%", # width of the map
                 height="85%", # height of the map
                 zoom_start=12, # the staring zoom
                 tiles="OpenStreetMap", # desired tile for the map respresentation
                 zoom_control=True) # controls for zoom level (True by default)
    
    # add a marker to the map for each station
    for station in stations:
        coordinates = (station.latitude, station.longitude)
        folium.Marker(coordinates).add_to(map)
        
    
    context = {'map': map._repr_html_()}
    return render(request, 'core/dashboard.html', context)

def fleet(request):
    products = Product.objects.all()
    return render(request, 'core/fleet.html', {'products': products})

def routes(request):
    stations = EVChargingLocation.objects.all()
    context = {
        'stations': stations,
        'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN,
    }
    return render(request, 'core/routes.html', context)

def stops(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'mapbox_access_token': settings.MAPBOX_ACCESS_TOKEN,
    }
    return render(request, 'core/stops.html', context)

def addproduct(request):
    products = Product.objects.all()
    form = AddProductForm(request.POST)
    return render(request, 'core/addproduct.html', {
        'form': form,
    }) 
    # return render(request, 'core/addproduct.html', {'products': products})
   
 
def addcompany(request):
    print(f'{request.POST = }')  
    if request.method == 'POST':
        # Process form data
        # You should use Django forms to validate and clean data
        company = Company.objects.create(
            name=request.POST.get('name'),
            desc=request.POST.get('desc'),
            isfeatured = request.POST.get('isfeatured') == 'on',
            isprivatelabel = request.POST.get('isprivatelabel') == 'on',
            isactive = request.POST.get('isactive') == 'on',
            cell_phone = request.POST.get('cellphone'),
            work_phone = request.POST.get('workphone'),
            email = request.POST.get('email'),
            website_url= request.POST.get('website'),
            # image = request.FILES.get('image')  # Handle file upload
            # Set other fields similarly
        )
        return JsonResponse({'message': 'Company added successfully!'})
    return render(request, 'core/addcompany.html')

        
def register_user(request):
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            # username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user) 
            messages.success(request, ("Registration successful"))
            return redirect('/')
    else:
        form = RegisterUserForm() 
    return render(request, 'core/register.html', {
        'form': form,
    }) 

def login_user(request):
    if request.method == "POST":
        # username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        # user = authenticate(request, username=username, password=password)
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            # Redirect to a success page.
            return redirect('/dashboard/')
        else:
            # Return an 'invalid login' error message.
            messages.success(request, ("There was an error"))
            return redirect('login')
    else:
        return render(request, 'core/login.html', {})


def logout_user(request):
    logout(request)
    messages.success(request, ("There was an error"))
    return redirect('/')
    
    
def registration(request):
    return render(request, 'core/registration.html')



User = get_user_model()


@api_view(['POST'])
@permission_classes([AllowAny])
def check_username_exists(request):
    if not request.data.get('username'):
        return Response({'error': 'Bad_request'}, status=status.HTTP_400_BAD_REQUEST)

    username = request.data.get('username')
    try:
        User.objects.get(username=username)
        return Response({'username_exists': True}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'username_exists': False}, status=status.HTTP_404_NOT_FOUND)
    
    
@api_view(['POST'])
@permission_classes([AllowAny])
def check_email_exists(request):
    if not request.data.get('email'):
        return Response({'error': 'Bad_request'}, status=status.HTTP_400_BAD_REQUEST)

    email = request.data.get('email')
    try:
        User.objects.get(email=email)
        return Response({'email_exists': True}, status=status.HTTP_200_OK)

    except User.DoesNotExist:
        return Response({'email_exists': False}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
def home(request):
    return Response({'detail': 'API status green'}, status=status.HTTP_200_OK)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        try:
            user = User.objects.get(email=request.data.get('email'))
            if not user.is_active:
                return Response({'detail': 'Account not activated'}, status=status.HTTP_401_UNAUTHORIZED)
            if user.is_deactivated:
                return Response({'detail': 'Account deactivated'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)

        return super().post(request, *args, **kwargs)
    
    
    
class ActivateUser(UserViewSet):
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs.setdefault('context', self.get_serializer_context())
 
        # this line is the only change from the base implementation.
        kwargs['data'] = {"uid": self.kwargs['uid'], "token": self.kwargs['token']}
 
        return serializer_class(*args, **kwargs)
 
    def activation(self, request, uid, token, *args, **kwargs):
        response = super().activation(request, *args, **kwargs)
        # Check if activation was successful, you might adjust this based on the actual response conditions
        if response.status_code == status.HTTP_204_NO_CONTENT:
            # Redirect to a custom success URL
            return redirect('activation_success')
        else:
            return response  # or you might redirect to an error page
        # return Response(status=status.HTTP_204_NO_CONTENT)
        

class StopCreateView(CreateView):
    model = Stop
    fields = [
        'title', 
        'description', 
        'origin_address',
        'origin_address_full',
        'origin_window_range_start',
        'origin_notes',
        'destination_address',
        'destination_address_full',
        'destination_window_range_start',
        'destination_notes',
        'ordering_number',
        'origin_tracking_number',
        'load_number',
        'manifest_number',
        'destination_tracking_number',
        'image',
        'thumbnail',
        'proof_of_pickup_picture_1',
        'proof_of_pickup_picture_1',
        'contact_user',
        'notes',
        ]
    template_name = 'core/fleet.html'
    success_url = 'core/dashboard.html'

def activation_success(request):
    return render(request, 'core/activation_success.html')


def reset_password(request):
    return render(request, 'core/reset_password.html')


# Product

class ProductBaseView(LoginRequiredMixin, View):
    model = Product
    fields = '__all__'
    success_url = reverse_lazy('products:all')

class ProductListView(ProductBaseView, ListView):
    """View to list all products.
    Use the 'product_list' variable in the template
    to access all Product objects"""

class ProductDetailView(ProductBaseView, DetailView):
    """View to list the details from one product.
    Use the 'product' variable in the template to access
    the specific product here and in the Views below"""

class ProductCreateView(ProductBaseView, CreateView):
    """View to create a new product"""

class ProductUpdateView(ProductBaseView, UpdateView):
    """View to update a product"""

class ProductDeleteView(ProductBaseView, DeleteView):
    """View to delete a product"""