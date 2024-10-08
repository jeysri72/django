# from django import forms
# from .models import Profile

# class ProfileForm(forms.ModelForm):
#     class Meta:
#         model = Profile
#         fields = '__all__'


from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator, RegexValidator
from django.utils import timezone
from .models import Profile

class ProfileForm(forms.ModelForm):
    # Validator for phone number field to ensure proper format
    phone_number_validator = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',  # Regular expression for phone number validation
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed."  # Custom error message
    )

    # Define form fields with widgets and custom error messages
    first_name = forms.CharField(
        max_length=50,  # Max length validation for first name
        required=True,  # The field is mandatory
        widget=forms.TextInput(attrs={'placeholder': 'First Name'}),  # Widget to display the input field
        error_messages={
            'required': 'First name is required',  # Custom error message for required field
            'max_length': 'First name cannot exceed 50 characters'  # Custom error message for max length
        }
    )

    last_name = forms.CharField(
        max_length=50,  # Max length validation for last name
        required=True,  # The field is mandatory
        widget=forms.TextInput(attrs={'placeholder': 'Last Name'}),
        error_messages={
            'required': 'Last name is required',
            'max_length': 'Last name cannot exceed 50 characters'
        }
    )

    email = forms.EmailField(
        required=True,  # The field is mandatory
        validators=[EmailValidator(message="Enter a valid email address.")],  # Built-in email validator
        widget=forms.EmailInput(attrs={'placeholder': 'Email'}),  # Widget to display an email input field
        error_messages={
            'required': 'Email is required',
            'invalid': 'Enter a valid email address'  # Custom error message for invalid email format
        }
    )

    phone_number = forms.CharField(
        required=True,  # Phone number is madatory
        validators=[phone_number_validator],  # Custom validator for phone number format
        widget=forms.TextInput(attrs={'placeholder': 'Phone Number'}),
        error_messages={
            'invalid': 'Enter a valid phone number format (+999999999).'  # Error message if regex validation fails
        }
    )

    date_of_birth = forms.DateField(
        required=True,  # Date of birth is mandatory
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Date of Birth'}),  # Widget to display date input field
        error_messages={
            'invalid': 'Enter a valid date of birth'  # Custom error message for invalid date
        }
    )

    address = forms.CharField(
        required=False,  # Address is optional
        widget=forms.Textarea(attrs={'placeholder': 'Address', 'rows': 3}),  # Widget to display a textarea
        error_messages={
            'max_length': 'Address cannot exceed 300 characters'  # Custom error message for address field
        }
    )

    enrollment_date = forms.DateField(
        required=True,  # The field is mandatory
        widget=forms.DateInput(attrs={'type': 'date', 'placeholder': 'Enrollment Date'}),
        error_messages={
            'required': 'Enrollment date is required',  # Custom error message for required field
            'invalid': 'Enter a valid enrollment date'  # Error message for invalid date format
        }
    )

    major = forms.CharField(
        max_length=100,  # Max length validation for major
        required=False,  # Major is optional
        widget=forms.TextInput(attrs={'placeholder': 'Major'}),
        error_messages={
            'max_length': 'Major cannot exceed 100 characters'  # Custom error message for max length
        }
    )

    status = forms.ChoiceField(
        choices=Profile.STATUS_CHOICES,  # Dropdown for status field choices (active, graduated, inactive)
        required=True,  # The field is mandatory
        widget=forms.Select(attrs={'placeholder': 'Status'}),  # Widget to display select box
        error_messages={
            'required': 'Status is required'  # Custom error message for required field
        }
    )

    class Meta:
        model = Profile  # Link form to the Student Profile model
        fields = '__all__'  # Include all fields from the model in the form

    # Custom validation method for email field
    def clean_email(self):
        email = self.cleaned_data.get('email')  # Get the value of the email field
        # if Profile.objects.filter(email=email).exists():  # Check if the email is already in use
        #     raise ValidationError("This email is already in use.")  # Raise validation error if email exists
        # return email  # Return cleaned data if validation passes

        # Check if the email already exists for a different profile
        if Profile.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise ValidationError("This email is already in use by another profile.")
        return email
    

    # Custom validation method for date of birth field
    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get('date_of_birth')  # Get the value of the date_of_birth field
        if date_of_birth and date_of_birth >= timezone.now().date():  # Ensure date is not in the future
            raise ValidationError("The date of birth cannot be in the future.")  # Raise validation error if invalid
        return date_of_birth  # Return cleaned data if validation passes

    # Custom validation method for enrollment date field
    def clean_enrollment_date(self):
        enrollment_date = self.cleaned_data.get('enrollment_date')  # Get the value of the enrollment_date field
        if enrollment_date and enrollment_date > timezone.now().date():  # Ensure enrollment date is not in the future
            raise ValidationError("Enrollment date cannot be in the future.")  # Raise validation error if invalid
        return enrollment_date  # Return cleaned data if validation passes

    # Custom validation method for phone number field
    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')  # Get the value of the phone_number field
        if phone_number and len(phone_number) < 9:  # Ensure phone number has at least 9 digits
            raise ValidationError("Phone number must contain at least 9 digits.")  # Raise validation error if invalid
        return phone_number  # Return cleaned data if validation passes
