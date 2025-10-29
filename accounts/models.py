from django.db import models
import uuid
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse


# ============================
# CUSTOM USER MODEL & MANAGER
# ============================

class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'superadmin')
        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    """Custom User model with email as username and role-based access"""

    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('vendor', 'Vendor'),
        ('customer', 'Customer'),
    )
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='customer')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, unique=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    phone_number = models.CharField(max_length=20, unique=True, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)

    # Status
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        ordering = ['username']
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    
    
    def is_vendor(self):
        return self.role == 'vendor'
    
    def is_customer(self):
        return self.role == 'customer'
    
    def is_superadmin(self):
        return self.role == 'superadmin'
    


    def __str__(self):
        return self.email

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    def get_short_name(self):
        return self.first_name or self.username


# ======================
# VENDOR & CUSTOMER MODELS
# ======================

class VendorProfile(models.Model):
    """Extended profile for vendors/real estate agents"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='vendor_profile')
    company_name = models.CharField(max_length=200, blank=True, null=True)
    business_address = models.TextField(blank=True, null=True)
    bio = models.TextField(max_length=1000, blank=True, null=True)
    rating = models.DecimalField(
        max_digits=3, decimal_places=2, default=0.00,
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    total_reviews = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - {self.company_name or 'Independent Vendor'}"


class CustomerProfile(models.Model):
    """Extended profile for customers/buyers"""
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='customer_profile')
    date_of_birth = models.DateField(blank=True, null=True)
    occupation = models.CharField(max_length=100, blank=True, null=True)
    preferred_location = models.CharField(max_length=200, blank=True, null=True)
    budget_min = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    budget_max = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.get_full_name()} - Customer Profile"


# ======================
# PROPERTY MANAGEMENT MODELS
# ======================

class Property(models.Model):
    """Main Property model representing real estate listings"""

    PROPERTY_TYPES = [
        ('apartment', 'Apartment'),
        ('house', 'House'),
        ('condo', 'Condominium'),
        ('townhouse', 'Townhouse'),
        ('land', 'Land'),
        ('commercial', 'Commercial'),
    ]

    LISTING_TYPES = [
        ('sale', 'For Sale'),
        ('rent', 'For Rent'),
        ('lease', 'For Lease'),
    ]

    STATUS_CHOICES = [
        ('available', 'Available'),
        ('pending', 'Pending'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
        ('inactive', 'Inactive'),
    ]

    # Basic Info
    title = models.CharField(max_length=200)
    description = models.TextField()
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES)
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')

    # Location
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

    # Pricing
    price = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default='NGN')

    # Property Details
    bedrooms = models.IntegerField(default=0)
    bathrooms = models.IntegerField(default=0)
    square_footage = models.IntegerField(blank=True, null=True)
    year_built = models.IntegerField(blank=True, null=True)

    # Vendor Relationship
    vendor = models.ForeignKey(
        VendorProfile,
        on_delete=models.CASCADE,
        related_name="properties"
    )

    # Meta
    is_featured = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.IntegerField(default=0)

    def get_absolute_url(self):
        return reverse('property_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"{self.title} - {self.city}"


class PropertyImage(models.Model):
    """Model for multiple property images"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='properties/')
    alt_text = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.property.title}"


class PropertyFeature(models.Model):
    """Extra features linked to a property"""
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='features')
    feature = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.property.title} - {self.feature}"
