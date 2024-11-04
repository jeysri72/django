from django.urls import path
from . import views

app_name = "contacts"
urlpatterns = [
    path('create-contact/', views.create_contact_view, name='create_contact'),
    path('get-contact/<str:email>/', views.get_contact_view, name='get_contact'),
    path('update-contact/<str:contact_id>/', views.update_contact_view, name='update_contact'),
    path('delete-contact/<str:contact_id>/', views.delete_contact_view, name='delete_contact'),
]
