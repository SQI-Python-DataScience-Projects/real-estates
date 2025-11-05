
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib import messages
from django.contrib.auth import (
    login, logout, authenticate,
    update_session_auth_hash, get_user_model
)
from django.contrib.auth.views import (
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.urls import reverse_lazy
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Generate auth token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

# Email utilities
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string

from .forms import (
    RegistrationForm, VendorRegistrationForm,
    CustomLoginForm,
    UserProfileForm, VendorProfileForm, CustomerProfileForm,
    CustomPasswordResetForm, CustomSetPasswordForm, PropertyForm
)
from .models import CustomUser, VendorProfile, CustomerProfile, Property


User = get_user_model()

# --------------------------------
# Homepage
# --------------------------------
def index(request):
    return render(request, "index.html")



# --------------------------------
# Registration
# --------------------------------
def register_vendor(request):
    if request.method == 'POST':
        form = VendorRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.role = 'vendor'

            VendorProfile.objects.create(user=user)  # Create vendor profile immediately
            # login(request, user)
            messages.success(request, "HI Vendor... You've registered successfully")
            return redirect('vendor_dashboard')

    else:
        form = VendorRegistrationForm()
    return render(request, 'register_vendor.html', {'form': form})

def register_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Generate token for email verification
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain
            verification_link = f"http://{domain}/activate/{uid}/{token}/"

            # Send verification email
            subject = f"Welcome {user.username}!"
            html_message = render_to_string("verification_email.html", {
                "user": user,
                "verification": verification_link
            })

            try:
                email = EmailMessage(
                    subject=subject,
                    from_email=settings.EMAIL_HOST_USER,
                    to=[user.email],
                    body=html_message
                )
                email.content_subtype = "html"
                email.send()
                print('Registration Successful!!!')
                messages.success(request, "A verification email has been sent. Please check your inbox.")
            except Exception as e:
                print(f"Failed to send email: {e}")
                messages.error(request, "Failed to send verification email.")
            
            return redirect("login")
    else:
        form = RegistrationForm()

    return render(request, "register.html", {"form": form})


# --------------------------------
# Account Activation
# --------------------------------
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully. You can now log in.")
        return redirect("login")
    else:
        messages.error(request, "Activation failed. Invalid or expired link.")
        return redirect("register")


# --------------------------------
# Login
# --------------------------------

def login_page(request):
    if request.method == "POST":
        form = CustomLoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request,user)
            messages.success(request, f"Welcome back, {username}!")

            # if user is not None:
            #     login(request,user)
            #     messages.success(request, f"Welcome back, {username}!")
            #     return redirect("index") 
            # else:
            #     messages.error(request, "Invalid username or password.")

            if user.role == 'vendor':
                return redirect('vendor_dashboard')
            elif user.role == 'customer':
                return redirect('customer_dashboard')
            elif user.role == 'superadmin':
                return redirect('admin_dashboard')

        else:
            messages.warning(request, "Invalid username or password.")

    else:
        form = CustomLoginForm()

    return render(request, "login.html",{"form":form})

        
    
# --------------------------------
# Logout
# --------------------------------
def logout_page(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("index")


# --------------------------------
# Profile Views
# --------------------------------
@login_required
def profile_view(request):
    """Display user profile"""
    user = request.user
    context = {'user': user}

    if user.role == 'vendor':
        vendor_profile, _ = VendorProfile.objects.get_or_create(user=user)
        context['vendor_profile'] = vendor_profile
    elif user.role == 'customer':
        customer_profile, _ = CustomerProfile.objects.get_or_create(user=user)
        context['customer_profile'] = customer_profile

    return render(request, 'profile.html', context)


@login_required
def edit_profile_view(request):
    """Edit user profile"""
    user = request.user

    if request.method == 'POST':
        user_form = UserProfileForm(request.POST, request.FILES, instance=user)

        # Role-specific form
        if user.role == 'vendor':
            profile, _ = VendorProfile.objects.get_or_create(user=user)
            profile_form = VendorProfileForm(request.POST, instance=profile)
        elif user.role == 'customer':
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
            profile_form = CustomerProfileForm(request.POST, instance=profile)
        else:
            profile_form = None

        if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
            user_form.save()
            if profile_form:
                profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserProfileForm(instance=user)
        if user.role == 'vendor':
            profile, _ = VendorProfile.objects.get_or_create(user=user)
            profile_form = VendorProfileForm(instance=profile)
        elif user.role == 'customer':
            profile, _ = CustomerProfile.objects.get_or_create(user=user)
            profile_form = CustomerProfileForm(instance=profile)
        else:
            profile_form = None

    return render(request, 'edit_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })


# --------------------------------
# Change Password
# --------------------------------
@login_required
def change_password_view(request):
    """Allow user to change password"""
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html', {'form': form})


# --------------------------------
# Password Reset Views
# --------------------------------
class CustomPasswordResetView(PasswordResetView):
    template_name = 'accounts/password_reset.html'
    email_template_name = 'accounts/password_reset_email.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    success_url = reverse_lazy('password_reset_done')
    form_class = CustomPasswordResetForm


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')
    form_class = CustomSetPasswordForm


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


def vendor_required(user):
    return user.is_authenticated and user.role == 'vendor'


# --------------------------------
# Vendor Property Management
# --------------------------------
from django.contrib.auth.decorators import user_passes_test

@login_required
@user_passes_test(vendor_required)

def vendor_property_list(request):
    if request.user.role == 'customer':
        messages.error(request, "Access denied. Only vendors can manage properties.")
        return redirect('index')
    
    vendor_profile = VendorProfile.objects.get(user=request.user)
    properties = vendor_profile.properties.all()

    
    
   # Apply filters
    property_type = request.GET.get('property_type', '').strip()
    status = request.GET.get('status', '').strip()
    
    if property_type:
        properties = properties.filter(property_type__iexact=property_type)
    
    if status == 'available':
        properties = properties.filter(status='available')
    elif status == 'unavailable':
        properties = properties.exclude(status='available')

    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(properties, 10)
    
    try:
        properties_page = paginator.page(page)
    except PageNotAnInteger:
        properties_page = paginator.page(1)
    except EmptyPage:
        properties_page = paginator.page(paginator.num_pages)
    
    return render(request, 'vendor_property_list.html', {
        'properties': properties_page,
        'property_type': property_type,
        'status': status,
    })

    
    
    
@user_passes_test(vendor_required)   
@login_required
def vendor_property_create(request):
    if request.user.role == 'customer':
        messages.error(request, "Access denied. Only vendors can add properties.")
        return redirect('index')

    vendor_profile = VendorProfile.objects.get(user=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            property_obj = form.save(commit=False)
            property_obj.vendor = vendor_profile
            property_obj.save()
            messages.success(request, "Property created successfully!")
            return redirect('vendor_property_list')
    else:
        form = PropertyForm()
    
    return render(request, 'vendor_property_form.html', {'form': form})

@user_passes_test(vendor_required)
@login_required
def vendor_property_update(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, vendor__user=request.user)
    
    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property_obj)
        if form.is_valid():
            form.save()
            messages.success(request, "Property updated successfully!")
            return redirect('vendor_property_list')
    else:
        form = PropertyForm(instance=property_obj)
    
    return render(request, 'update_vendor_property_form.html', {'form': form})

@user_passes_test(vendor_required)
@login_required
def vendor_property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, vendor__user=request.user)
    property_obj.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect('vendor_property_list')



@login_required
def vendor_dashboard(request):
    """Vendor Dashboard - ONLY for vendors"""
    # Redirect non-vendors
    if request.user.role != 'vendor':
        messages.warning(request, "Access denied. You don't have vendor privileges.")
        if request.user.role == 'customer':
            return redirect('customer_dashboard')
        elif request.user.role == 'superadmin':
            return redirect('admin_dashboard')
        else:
            return redirect('index')
    
    # Get vendor profile
    vendor_profile = VendorProfile.objects.get(user=request.user)
    
    # Get vendor properties
    vendor_properties = Property.objects.filter(vendor=vendor_profile)
    
    # Calculate statistics
    total_properties = vendor_properties.count()
    active_listings = vendor_properties.filter(status='available').count()
    
    # Calculate total views
    total_views = 0
    for prop in vendor_properties:
        if hasattr(prop, 'views_count'):
            total_views += prop.views_count or 0
        elif hasattr(prop, 'views'):
            total_views += prop.views or 0
    
    # Get recent properties
    recent_properties = vendor_properties.order_by('-created_at')[:5]
    
    context = {
        'vendor_profile': vendor_profile,
        'total_properties': total_properties,
        'active_listings': active_listings,
        'total_views': total_views,
        'recent_properties': recent_properties,
        'recent_inquiries': [],
    }
    
    return render(request, 'vendor_dashboard.html', context)


@login_required
def customer_dashboard(request):
    """Customer Dashboard - ONLY for customers"""
    # Redirect non-customers
    if request.user.role != 'customer':
        messages.warning(request, "Access denied. This is for customers only.")
        if request.user.role == 'vendor':
            return redirect('vendor_dashboard')
        elif request.user.role == 'superadmin':
            return redirect('admin_dashboard')
        else:
            return redirect('index')
    
    # Get or create customer profile
    customer_profile, created = CustomerProfile.objects.get_or_create(user=request.user)
    
    # Get customer data
    saved_properties = []
    recent_inquiries = []
    recommended_properties = Property.objects.filter(status='available')[:4]
    
    context = {
        'customer_profile': customer_profile,
        'saved_properties_count': 0,
        'active_inquiries': 0,
        'properties_viewed': 0,
        'reviews_written': 0,
        'saved_properties': saved_properties,
        'recent_inquiries': recent_inquiries,
        'recommended_properties': recommended_properties,
        'recent_searches': [],
    }
    
    return render(request, 'customer_dashboard.html', context)


@login_required
def admin_dashboard(request):
    """Admin Dashboard - ONLY for admins"""
    # Redirect non-admins
    if request.user.role != 'superadmin':
        messages.warning(request, "Access denied. Admin privileges required.")
        if request.user.role == 'vendor':
            return redirect('vendor_dashboard')
        elif request.user.role == 'customer':
            return redirect('customer_dashboard')
        else:
            return redirect('index')
    
    # Admin statistics
    total_users = CustomUser.objects.count()
    total_vendors = CustomUser.objects.filter(role='vendor').count()
    total_customers = CustomUser.objects.filter(role='customer').count()
    total_properties = Property.objects.count()
    
    context = {
        'total_users': total_users,
        'total_vendors': total_vendors,
        'total_customers': total_customers,
        'total_properties': total_properties,
    }
    
    return render(request, 'admin_dashboard.html', context)

# --------------------------------
# Property Search & Filter View
# --------------------------------
def property_search(request):
    """
    Search and filter properties with query parameters
    Supports: location, price range, property type, pagination
    """
    # properties = Property.objects.filter('available').select_related('vendor__user')
    properties = Property.objects.filter(status='available').select_related('vendor__user')

    
    # Get query parameters
    location = request.GET.get('location', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    search_query = request.GET.get('q', '').strip()
    
    # Apply filters
    if location:
        properties = properties.filter(
            Q(city__icontains=location) | 
            Q(state__icontains=location) |
            Q(address__icontains=location)
        )
    
    if min_price:
        try:
            properties = properties.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            properties = properties.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    if property_type:
        properties = properties.filter(property_type__iexact=property_type)
    
    if search_query:
        properties = properties.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(address__icontains=search_query)
        )
    
    # Order by newest first
    properties = properties.order_by('-created_at')
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(properties, 12)  # 12 properties per page
    
    try:
        properties_page = paginator.page(page)
    except PageNotAnInteger:
        properties_page = paginator.page(1)
    except EmptyPage:
        properties_page = paginator.page(paginator.num_pages)
    
    # Get distinct property types for filter dropdown
    property_types = Property.objects.values_list('property_type', flat=True).distinct()
    
    context = {
        'properties': properties_page,
        'property_types': property_types,
        'location': location,
        'min_price': min_price,
        'max_price': max_price,
        'property_type': property_type,
        'search_query': search_query,
        'total_results': paginator.count,
    }
    
    return render(request, 'property_search.html', context)


# --------------------------------
# Property Detail View
# --------------------------------
def property_detail(request, pk):
    """View individual property details"""
    property_obj = get_object_or_404(Property, pk=pk)
    
    # Get similar properties (same type, nearby location)
    similar_properties = Property.objects.filter(
        property_type=property_obj.property_type,
        status='available'

    ).exclude(pk=pk)[:4]
    
    context = {
        'property': property_obj,
        'similar_properties': similar_properties,
    }
    
    return render(request, 'property_detail.html', context)


# --------------------------------
# API Endpoint for Property Filtering (JSON Response)
# --------------------------------
def property_api(request):
    """
    REST API endpoint for property filtering
    Returns JSON response for AJAX calls or API consumers
    """
    # properties = Property.objects.filter(is_available=True)
    properties = Property.objects.filter(status='available')

    
    # Apply filters
    location = request.GET.get('location', '').strip()
    min_price = request.GET.get('min_price', '').strip()
    max_price = request.GET.get('max_price', '').strip()
    property_type = request.GET.get('property_type', '').strip()
    
    if location:
        properties = properties.filter(
            Q(city__icontains=location) | 
            Q(state__icontains=location) |
            Q(address__icontains=location)
        )
    
    if min_price:
        try:
            properties = properties.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            properties = properties.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    if property_type:
        properties = properties.filter(property_type__iexact=property_type)
    
    # Pagination
    page = request.GET.get('page', 1)
    paginator = Paginator(properties, 12)
    
    try:
        properties_page = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        properties_page = paginator.page(1)
    
    # Serialize data
    data = {
        'count': paginator.count,
        'num_pages': paginator.num_pages,
        'current_page': properties_page.number,
        'has_next': properties_page.has_next(),
        'has_previous': properties_page.has_previous(),
        'results': [
            {
                'id': prop.id,
                'title': prop.title,
                'description': prop.description,
                'property_type': prop.property_type,
                'price': str(prop.price),
                'address': prop.address,
                'city': prop.city,
                'state': prop.state,
                'bedrooms': prop.bedrooms,
                'bathrooms': prop.bathrooms,
                'area': str(prop.area),
                'is_available': prop.status == 'available',
                'vendor': prop.vendor.user.get_full_name() or prop.vendor.user.username,
            }
            for prop in properties_page
        ]
    }
    
    return JsonResponse(data)
# @login_required
# @user_passes_test(vendor_required)
# def vendor_dashboard(request):
#     return render(request, 'vendor_dashboard.html')

# @login_required
# def customer_dashboard(request):
#     return render(request, 'customer_dashboard.html')

# @login_required
# @user_passes_test(lambda u: u.role == 'admin')
# def admin_dashboard(request):
#     return render(request, 'admin_dashboard.html')
