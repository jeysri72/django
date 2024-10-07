from django.urls import path
from helloworld_app import views

app_name = "helloworld_app"

urlpatterns = [
    path("", views.home, name="home"),
]
