from django import forms
from .models import Customer, Product, CartItem, Feedback

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


class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['qty', 'discount']

    def clean_qty(self):
        qty = self.cleaned_data['qty']
        if qty < 1:
            raise forms.ValidationError("Quantity must be at least 1.")
        return qty

    def clean_discount(self):
        discount = self.cleaned_data['discount']
        if discount < 0:
            raise forms.ValidationError("Discount cannot be negative.")
        return discount


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ['comments']
        widgets = {
            'comments': forms.Textarea(attrs={'placeholder': 'Your feedback...', 'rows': 5}),
        }