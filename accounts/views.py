# from django.shortcuts import render,redirect
# from django.http import HttpResponse
# from django.contrib import messages
# from django.contrib.auth import login,logout,authenticate,update_session_auth_hash, get_user_model
# from django.contrib.auth.views import (
#     PasswordResetView, PasswordResetDoneView, 
#     PasswordResetConfirmView, PasswordResetCompleteView
# )
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.forms import PasswordChangeForm
# from django.urls import reverse_lazy

# #Generate auth token
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes, force_str
# from django.contrib.auth.tokens import default_token_generator
# from django.contrib.sites.shortcuts import get_current_site

# #Function for sending welcome mail
# from django.core.mail import send_mail, EmailMessage
# from django.conf import settings
# from django.template.loader import render_to_string

# from .forms import (
#     RegistrationForm, CustomLoginForm,
#     UserProfileForm, VendorProfileForm, CustomerProfileForm,
#     CustomPasswordResetForm, CustomSetPasswordForm
# )
# from .models import CustomUser, VendorProfile, CustomerProfile

# User = get_user_model()
# # Create your views here.
# def index(request):
#     return render(request, "index.html")

# # Registration
# def register_page(request):
#     if request.method == "POST":
        
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = False
#             user.save()

#             # Generate token to be used for verification
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)
#             domain = get_current_site(request).domain
#             verification_link = f"http://{domain}/activate/{uid}/{token}"


#             # Send mail
#             subject = f"Hello {user.username}"
#             html_message = render_to_string("verification_email.html",{"user":user, "verification":verification_link})
#             try:
#                 email = EmailMessage(
#                     subject=subject,
#                     from_email=settings.EMAIL_HOST_USER,
#                     to=[user.email],
#                     body=html_message
#                 )
#                 email.content_subtype = "html"
#                 email.send()
#                 print('Registration Successful!!!')
#                 messages.success(request, "A verification email has been sent. Please check your inbox.")

#             except Exception as e:
#                 print(f"Failed to send email: {e}")     
#                 messages.error(request, "Failed to send a message...")
#             finally:
#                 form = RegistrationForm()
#                 return redirect("login")  
            
#     else:
#         form = RegistrationForm()

#     return render(request, "register.html",{"form":form})



# # Function to activate email
# from django.contrib.auth import get_user_model
# User = get_user_model()

# def activate_account(request,uid64,token):
#     try:
#         uid = force_str(urlsafe_base64_decode(uid64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None

#     if user and default_token_generator.check_token(user,token):
#         user.is_active = True
#         user.save()
#         messages.success(request,"Account Activated")
#         return redirect("login")
#     else:
#         messages.error("Activation Failed")
#         return redirect("register")


# # Login 
# def login_page(request):
#     if request.method == "POST":
#         form = CustomLoginForm(request,data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get("username")
#             password = form.cleaned_data.get("password")
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request,user)
#                 messages.success(request, f"Welcome back, {username}!")
#                 return redirect("index") 
#             else:
#                 messages.error(request, "Invalid username or password.")
#         else:
#             messages.warning(request, "Invalid username or password.")

#     else:
#         form = CustomLoginForm()

#     return render(request, "login.html",{"form":form})

# # Logout
# def logout_page(request):
#     logout(request)
#     return redirect("index")



# @login_required
# def profile_view(request):
#     """Display user profile"""
#     user = request.user
#     context = {'user': user}
    
#     # Get or create profile based on role
#     if user.role == 'vendor':
#         vendor_profile, created = VendorProfile.objects.get_or_create(user=user)
#         context['vendor_profile'] = vendor_profile
#     elif user.role == 'customer':
#         customer_profile, created = CustomerProfile.objects.get_or_create(user=user)
#         context['customer_profile'] = customer_profile
    
#     return render(request, 'profile.html', context)


# @login_required
# def edit_profile_view(request):
#     """Edit user profile (both basic info and role-specific info)"""
#     user = request.user
    
#     if request.method == 'POST':
#         user_form = UserProfileForm(request.POST, request.FILES, instance=user)
        
#         # Handle role-specific profile
#         if user.role == 'vendor':
#             vendor_profile, created = VendorProfile.objects.get_or_create(user=user)
#             profile_form = VendorProfileForm(request.POST, instance=vendor_profile)
#         elif user.role == 'customer':
#             customer_profile, created = CustomerProfile.objects.get_or_create(user=user)
#             profile_form = CustomerProfileForm(request.POST, instance=customer_profile)
#         else:
#             profile_form = None
        
#         # Validate and save both forms
#         if user_form.is_valid() and (profile_form is None or profile_form.is_valid()):
#             user_form.save()
#             if profile_form:
#                 profile_form.save()
#             messages.success(request, 'Profile updated successfully!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         user_form = UserProfileForm(instance=user)
        
#         # Load role-specific profile form
#         if user.role == 'vendor':
#             vendor_profile, created = VendorProfile.objects.get_or_create(user=user)
#             profile_form = VendorProfileForm(instance=vendor_profile)
#         elif user.role == 'customer':
#             customer_profile, created = CustomerProfile.objects.get_or_create(user=user)
#             profile_form = CustomerProfileForm(instance=customer_profile)
#         else:
#             profile_form = None
    
#     context = {
#         'user_form': user_form,
#         'profile_form': profile_form,
#     }
#     return render(request, 'edit_profile.html', context)

# @login_required
# def change_password_view(request):
#     """Handle password change for logged-in users"""
#     if request.method == 'POST':
#         form = PasswordChangeForm(request.user, request.POST)
#         if form.is_valid():
#             user = form.save()
#             update_session_auth_hash(request, user)  
#             messages.success(request, 'Your password was successfully updated!')
#             return redirect('profile')
#         else:
#             messages.error(request, 'Please correct the errors below.')
#     else:
#         form = PasswordChangeForm(request.user)
    
#     return render(request, 'change_password.html', {'form': form})


# # Password Reset Views
# class CustomPasswordResetView(PasswordResetView):
#     """Custom password reset view"""
#     template_name = 'accounts/password_reset.html'
#     email_template_name = 'accounts/password_reset_email.html'
#     subject_template_name = 'accounts/password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
#     form_class = CustomPasswordResetForm


# class CustomPasswordResetDoneView(PasswordResetDoneView):
#     """Password reset done view"""
#     template_name = 'password_reset_done.html'


# class CustomPasswordResetConfirmView(PasswordResetConfirmView):
#     """Password reset confirm view"""
#     template_name = 'password_reset_confirm.html'
#     success_url = reverse_lazy('password_reset_complete')
#     form_class = CustomSetPasswordForm


# class CustomPasswordResetCompleteView(PasswordResetCompleteView):
#     """Password reset complete view"""
#     template_name = 'password_reset_complete.html'
    
    
    
    
    
    
    
# from django.shortcuts import render, redirect, get_object_or_404
# from django.contrib.auth.decorators import login_required
# from django.contrib import messages
# from .models import Property, VendorProfile
# from .forms import PropertyForm

# @login_required
# def vendor_property_list(request):
#     if request.user.role != 'vendor':
#         messages.error(request, "Access denied. Only vendors can manage properties.")
#         return redirect('home')
    
#     vendor_profile = VendorProfile.objects.get(user=request.user)
#     properties = vendor_profile.properties.all()
#     return render(request, 'properties/vendor_property_list.html', {'properties': properties})


# @login_required
# def vendor_property_create(request):
#     if request.user.role != 'vendor':
#         messages.error(request, "Access denied. Only vendors can add properties.")
#         return redirect('home')

#     vendor_profile = VendorProfile.objects.get(user=request.user)
    
#     if request.method == 'POST':
#         form = PropertyForm(request.POST, request.FILES)
#         if form.is_valid():
#             property_obj = form.save(commit=False)
#             property_obj.vendor = vendor_profile
#             property_obj.save()
#             messages.success(request, "Property created successfully!")
#             return redirect('vendor_property_list')
#     else:
#         form = PropertyForm()
    
#     return render(request, 'properties/vendor_property_form.html', {'form': form})


# @login_required
# def vendor_property_update(request, pk):
#     property_obj = get_object_or_404(Property, pk=pk, vendor__user=request.user)
    
#     if request.method == 'POST':
#         form = PropertyForm(request.POST, request.FILES, instance=property_obj)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Property updated successfully!")
#             return redirect('vendor_property_list')
#     else:
#         form = PropertyForm(instance=property_obj)
    
#     return render(request, 'properties/vendor_property_form.html', {'form': form})


# @login_required
# def vendor_property_delete(request, pk):
#     property_obj = get_object_or_404(Property, pk=pk, vendor__user=request.user)
#     property_obj.delete()
#     messages.success(request, "Property deleted successfully.")
#     return redirect('vendor_property_list')

from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
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
    RegistrationForm, CustomLoginForm,
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
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("index")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    else:
        form = CustomLoginForm()

    return render(request, "login.html", {"form": form})


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


# --------------------------------
# Vendor Property Management
# --------------------------------
@login_required
def vendor_property_list(request):
    if request.user.role == 'customer':
        messages.error(request, "Access denied. Only vendors can manage properties.")
        return redirect('index')
    
    vendor_profile = VendorProfile.objects.get(user=request.user)
    properties = vendor_profile.properties.all()
    return render(request, 'vendor_property_list.html', {'properties': properties})
    
    


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


@login_required
def vendor_property_delete(request, pk):
    property_obj = get_object_or_404(Property, pk=pk, vendor__user=request.user)
    property_obj.delete()
    messages.success(request, "Property deleted successfully.")
    return redirect('vendor_property_list')





