from django.shortcuts import render

# Create your views here.

def blog_page(request):
    return render(request,"blog.html")

def listings_page(request):
    return render(request,"listings.html")

def single_blog_page(request):
    return render(request,"single-blog.html")

def single_listings_page(request):
    return render(request,"single-listings.html")

def about_us_page(request):
    return render(request,"about-us.html")

def contact_page(request):
    return render(request,"contact.html")

def elements_page(request):
    return render(request,"elements.html")

