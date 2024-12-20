from django import forms
from .models import User, Product, Purchase

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'description', 'price']


class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ['user', 'product']
