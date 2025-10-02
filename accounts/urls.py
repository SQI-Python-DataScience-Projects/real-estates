from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),              # Homepage
    path("login/", views.login_page, name="login"),   # Login page
    path("register/", views.register_page, name="register"),  # Register page
    path("logout/", views.logout_page, name="logout"),  # Register page
    path('activate/<uid64>/<token>/', views.activate_account, name="activate")
]
