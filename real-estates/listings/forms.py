from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, PasswordResetForm,
    SetPasswordForm, AuthenticationForm
)
from .models import (
    CustomUser, VendorProfile, CustomerProfile,
    Property, PropertyImage, PropertyFeature
)



class PropertyForm(forms.ModelForm):
    """Form for creating or editing property details"""
    class Meta:
        model = Property
        fields = [
            'title', 'description', 'property_type', 'listing_type', 'status',
            'address', 'city', 'state', 'price', 'currency',
            'bedrooms', 'bathrooms', 'square_footage', 'year_built',
            'is_featured', 'is_verified'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Describe the property...'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Property Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'currency': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Currency'}),
            'square_footage': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Square Footage'}),
            'year_built': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Year Built'}),
        }
