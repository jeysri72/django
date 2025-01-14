# contacts/urls.py
from django.urls import path
from .views import upload_contacts, upload_csv

app_name = 'contacts_uploader'

urlpatterns = [
    path("", upload_contacts, name="upload_contacts"),
    path('upload_csv/', upload_csv, name='upload_csv'),
]
