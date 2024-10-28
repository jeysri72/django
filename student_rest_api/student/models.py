from django.db import models

# Create your models here.


class Profile(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('graduated', 'Graduated'),
        ('inactive', 'Inactive'),
    ]

    # Basic Information
    first_name = models.CharField(max_length=50) 
    last_name = models.CharField(max_length=50) 
    email = models.EmailField(unique=True) 

    # Optional fields
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    # Enrollment Information
    enrollment_date = models.DateField()
    major = models.CharField(max_length=100, blank=True, null=True)

    # Status with predefined choices
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
