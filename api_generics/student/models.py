from django.db import models

# Create your models here.
from django.db import models

# Create your models here.


class Profile(models.Model):

    # Basic Information
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    email = models.EmailField(unique=True) 

   

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
