
# Create your models here.
from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    contact = models.CharField(max_length=15)
    address = models.TextField()
    status = models.CharField(max_length=50)

class Product(models.Model):
    code = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    qty = models.PositiveIntegerField()



class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Overall discount
    total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the cart total
        items = self.items.all()  # Use related_name from CartItem
        self.discount = sum(item.discount for item in items)  # Sum of item discounts
        self.total = sum(item.line_total for item in items)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Cart for {self.customer} - Total: {self.total}"




class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Price per unit
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Discount per unit
    line_total = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        # Calculate the line total
        self.line_total =(self.price * self.qty) - self.discount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product} - {self.qty} units"


class PurchaseHeader(models.Model):
    purchase_date = models.DateTimeField(auto_now_add=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=10, decimal_places=2)

class PurchaseDetail(models.Model):
    purchaseHeader = models.ForeignKey(PurchaseHeader, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    description = models.TextField()
    qty = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    line_total = models.DecimalField(max_digits=10, decimal_places=2)

class Feedback(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    comments = models.TextField()
    sentiment_score = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    sentiment = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)



