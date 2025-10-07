# from django.urls import path
# from . import views

# urlpatterns = [
#     path("", views.index, name="index"),              # Homepage
#     path("login/", views.login_page, name="login"),   # Login page
#     path("register/", views.register_page, name="register"),  # Register page
#     path("logout/", views.logout_page, name="logout"),  # Register page
#     path('activate/<uid64>/<token>/', views.activate_account, name="activate"),

    
#     # Profile Management
#     path('profile/', views.profile_view, name='profile'),
#     path('profile/edit/', views.edit_profile_view, name='edit_profile'),
    
#     # Password Management
#     path('password/change/', views.change_password_view, name='change_password'),
#     path('password/reset/', views.CustomPasswordResetView.as_view(), name='password_reset'),
#     path('password/reset/done/', views.CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
#     path('password/reset/confirm/<uidb64>/<token>/', views.CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
#     path('password/reset/complete/', views.CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    
    
    
    
#     path('vendor/properties/', views.vendor_property_list, name='vendor_property_list'),
#     path('vendor/properties/add/', views.vendor_property_create, name='vendor_property_create'),
#     path('vendor/properties/<uuid:pk>/edit/', views.vendor_property_update, name='vendor_property_update'),
#     path('vendor/properties/<uuid:pk>/delete/', views.vendor_property_delete, name='vendor_property_delete'),
# ]



from django.urls import path
from . import views

urlpatterns = [
    # Authentication and User Management
    path("", views.index, name="index"),  # Homepage
    path("login/", views.login_page, name="login"),  # Login page
    path("register/", views.register_page, name="register"),  # Register page
    path("logout/", views.logout_page, name="logout"),  # Logout page

    # Account Activation
    path("activate/<uidb64>/<token>/", views.activate_account, name="activate"),

    # Profile Management
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.edit_profile_view, name="edit_profile"),

    # Password Management
    path("password/change/", views.change_password_view, name="change_password"),
    path("password/reset/", views.CustomPasswordResetView.as_view(), name="password_reset"),
    path("password/reset/done/", views.CustomPasswordResetDoneView.as_view(), name="password_reset_done"),
    path("password/reset/confirm/<uidb64>/<token>/", views.CustomPasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path("password/reset/complete/", views.CustomPasswordResetCompleteView.as_view(), name="password_reset_complete"),

    # Vendor Property Management
    path("vendor/properties/", views.vendor_property_list, name="vendor_property_list"),
    path("vendor/properties/add/", views.vendor_property_create, name="vendor_property_create"),
    path("vendor/properties/<uuid:pk>/edit/", views.vendor_property_update, name="vendor_property_update"),
    path("vendor/properties/<uuid:pk>/delete/", views.vendor_property_delete, name="vendor_property_delete"),
]




