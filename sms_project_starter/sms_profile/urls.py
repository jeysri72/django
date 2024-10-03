from django.urls import path
from . import views

app_name = 'sms_profile'  # This defines the namespace

urlpatterns = [
    path('', views.index, name='index'),
]
