from django.contrib import admin
from .models import CustomUser
from .models import UserManager

# Register your models here.
admin.site.register(CustomUser)

