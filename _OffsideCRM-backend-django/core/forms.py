from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from .models import Product
from .models import Company
from .models import Stop

User = get_user_model()

class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=255, required=True)
    
    class Meta: 
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
        
        
class AddProductForm(ModelForm):
   class Meta:
       model = Product
       fields = (
           'cat', 
           'name', 
           'slug', 
           'description', 
           'price', 
           'created_user', 
           'image',
           'thumbnail', 
           )
       labels = {
            'cat': '',
            'name': '',
            'slug': '', 
            'description': '', 
            'price': '', 
            'created_user': '', 
            'image': '',
            'thumbnail': '', 
        }

class AddCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = (
            'name',
            'desc',
            'isfeatured',
            'isprivatelabel',
            'isactive',
            'owner',
            'address',
            'company_type',
            'upvotes',
            'downvotes',
            'cell_phone',
            'work_phone',
            'email',
            'website_url',
            'image',
            'thumbnail',
        )
        
class StopForm(forms.ModelForm):
    class Meta:
        model = Stop
        exclude = (
            'id',
        )