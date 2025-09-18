from django import forms
from .models import Fertilizer,SoilType, Crop
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField
import re


from django import forms
from .models import Fertilizer

class FertilizerForm(forms.ModelForm):
    class Meta:
        model = Fertilizer
        fields = ['name', 'type', 'quantity', 'price', 'manufacturer', 'image', 'description']  # Include 'description'



class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email.endswith('@gmail.com'):
            raise forms.ValidationError("Please use a Gmail address.")
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email

    def clean_password1(self):
        password = self.cleaned_data.get('password1')
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        if not re.search(r'[A-Z]', password):
            raise forms.ValidationError("Password must contain at least one uppercase letter.")
        if not re.search(r'[a-z]', password):
            raise forms.ValidationError("Password must contain at least one lowercase letter.")
        if not re.search(r'[0-9]', password):
            raise forms.ValidationError("Password must contain at least one number.")
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise forms.ValidationError("Password must contain at least one special character.")
        return password

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove help text for all fields
        for field_name in self.fields:
            self.fields[field_name].help_text = None

class userloginForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    password = forms.CharField(widget=forms.PasswordInput, required=True)
    captcha = CaptchaField()

from django import forms
from .models import SoilType

class SoilTypeForm(forms.ModelForm):
    class Meta:
        model = SoilType
        fields = ['name', 'description', 'ph_range']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter soil type name'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
            'ph_range': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter pH range'}),
        }
from django import forms
from .models import Crop

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'ideal_soil', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter crop name'}),
            'ideal_soil': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter description', 'rows': 4}),
        }

from django import forms
from .models import Recommendation

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['crop', 'soil_type', 'suitable_fertilizers']
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-control'}),
            'soil_type': forms.Select(attrs={'class': 'form-control'}),
            'suitable_fertilizers': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }


from django import forms
from .models import Sale, Payment

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['farmer_name', 'contact_number', 'aadhar_number', 'address', 'fertilizer', 'quantity_sold', 'unit_price']

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['sale', 'amount', 'payment_method']
