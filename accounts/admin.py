from django.contrib import admin
from .models import CustomUser, VendorProfile, CustomerProfile,Property, PropertyImage, PropertyFeature
from django.contrib.auth.admin import UserAdmin

# Register your models here.


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'username', 'role', 'is_active', 'created_at']
    list_filter = ['role', 'is_active']
    search_fields = ['email', 'username']

@admin.register(VendorProfile)
class VendorProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'company_name', 'rating', 'total_reviews']

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'occupation', 'preferred_location']

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'property_type', 'listing_type', 'status', 'price', 'city', 'vendor', 'is_featured', 'created_at']
    list_filter = ['property_type', 'listing_type', 'status', 'is_featured', 'is_verified', 'created_at']
    search_fields = ['title', 'city', 'state', 'vendor__email']

@admin.register(PropertyImage)
class PropertyImageAdmin(admin.ModelAdmin):
    list_display = ['property', 'alt_text', 'created_at']
    list_filter = ['created_at']
    search_fields = ['property__title', 'alt_text']


@admin.register(PropertyFeature)
class PropertyFeatureAdmin(admin.ModelAdmin):
    list_display = ['property', 'feature']