from django.urls import path
from .views import landing_page, about_page, services_page, contact_page


urlpatterns = [
    path('', landing_page, name='landing_page'),
    path('home/', landing_page, name='landing_page'),
    path('about/', about_page, name='about'),
    path('services/', services_page, name='services'),
    path('contact/', contact_page, name='contact'),
]
