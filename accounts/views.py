from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import RegistrationForm, CustomLoginForm
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate

#Generate auth token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site

#Function for sending welcome mail
from django.core.mail import send_mail, EmailMessage
from django.conf import settings
from django.template.loader import render_to_string


# Create your views here.
def index(request):
    return render(request, "index.html")

# Registration
def register_page(request):
    if request.method == "POST":
        
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            # Generate token to be used for verification
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            domain = get_current_site(request).domain
            verification_link = f"http://{domain}/activate/{uid}/{token}"


            # Send mail
            subject = f"Hello {user.username}"
            html_message = render_to_string("verification_email.html",{"user":user, "verification":verification_link})
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
                messages.error(request, "Failed to send a message...")
            finally:
                form = RegistrationForm()
                return redirect("login")  
            
    else:
        form = RegistrationForm()

    return render(request, "register.html",{"form":form})



# Function to activate email
from django.contrib.auth import get_user_model
User = get_user_model()

def activate_account(request,ui64,token):
    try:
        uid = force_str(urlsafe_base64_decode(ui64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,"Account Activated")
        return redirect("login")
    else:
        messages.error("Activation Failed")
        return redirect("register")


# Login 
def login_page(request):
    if request.method == "POST":
        form = CustomLoginForm(request,data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request,user)
                messages.success(request, f"Welcome back, {username}!")
                return redirect("index") 
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.warning(request, "Invalid username or password.")

    else:
        form = CustomLoginForm()

    return render(request, "login.html",{"form":form})

# Logout
def logout_page(request):
    logout(request)
    return redirect("index")
