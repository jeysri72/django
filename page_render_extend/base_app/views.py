from django.shortcuts import render

# Create your views here.

# Landing Page
def landing_page(request):
    return render(request, 'base_app/landing.html')

# Inner Pages
def about_page(request):
    return render(request, 'base_app/about.html')

def services_page(request):
    return render(request, 'base_app/services.html')

def contact_page(request):
    return render(request, 'base_app/contact.html')
