from django import forms
from .models import Customer, Product

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['name', 'email', 'contact', 'address', 'status']

class ProductForm(forms.ModelForm):

    prompt = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter prompt here'})
    )  # Non-persistent field


    class Meta:
        model = Product
        fields = ['code', 'description', 'price', 'qty']
