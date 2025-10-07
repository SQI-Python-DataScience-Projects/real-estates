from django import forms
from django.contrib.auth.forms import (
    UserCreationForm, UserChangeForm, PasswordResetForm,
    SetPasswordForm, AuthenticationForm
)
from .models import (
    CustomUser, VendorProfile, CustomerProfile,
    Property, PropertyImage, PropertyFeature
)


# ===========================
# AUTHENTICATION & USER FORMS
# ===========================

class RegistrationForm(UserCreationForm):
    username = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"class": "form-control"})
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )
    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = CustomUser
        fields = ("username", "email", "password1", "password2")


class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=40,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control"})
    )


class CustomUserCreationForm(UserCreationForm):
    """Form for creating new users"""
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'first_name', 'last_name', 'role')


class CustomUserChangeForm(UserChangeForm):
    """Form for updating users"""
    class Meta:
        model = CustomUser
        fields = (
            'email', 'username', 'first_name', 'last_name',
            'phone_number', 'profile_image'
        )


class UserProfileForm(forms.ModelForm):
    """Form for updating user profile"""
    class Meta:
        model = CustomUser
        fields = [
            'first_name', 'last_name', 'username',
            'phone_number', 'profile_image'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
            'profile_image': forms.FileInput(attrs={'class': 'form-control'}),
        }


# ======================
# VENDOR & CUSTOMER FORMS
# ======================

class VendorProfileForm(forms.ModelForm):
    """Form for updating vendor profile"""
    class Meta:
        model = VendorProfile
        fields = ['company_name', 'business_address', 'bio']
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'business_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Business Address'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'Tell us about yourself and your business'}),
        }


class CustomerProfileForm(forms.ModelForm):
    """Form for updating customer profile"""
    class Meta:
        model = CustomerProfile
        fields = ['date_of_birth', 'occupation', 'preferred_location', 'budget_min', 'budget_max']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'occupation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Occupation'}),
            'preferred_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Preferred Location'}),
            'budget_min': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Minimum Budget'}),
            'budget_max': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Maximum Budget'}),
        }


# ====================
# PASSWORD RESET FORMS
# ====================

class CustomPasswordResetForm(PasswordResetForm):
    """Custom password reset form with styling"""
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your email address',
            'autocomplete': 'email'
        })
    )


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form with styling"""
    new_password1 = forms.CharField(
        label="New password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'New Password',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )
    new_password2 = forms.CharField(
        label="Confirm password",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Confirm New Password',
            'autocomplete': 'new-password'
        }),
        strip=False,
    )


# =====================
# PROPERTY MANAGEMENT
# =====================

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
