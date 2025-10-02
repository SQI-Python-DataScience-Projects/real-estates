from django.urls import path
from . import views

urlpatterns = [
    path("blog",views.blog_page,name="blog"),
    path("listings",views.listings_page,name="listings"),
    path("single-blog",views.single_blog_page,name="single-blog"),
    path("single-listings",views.single_listings_page,name="single-listings"),
    path("about-us",views.about_us_page,name="about-us"),
    path("contact",views.contact_page,name="contact"),
    path("elements",views.elements_page,name="elements"),
]
