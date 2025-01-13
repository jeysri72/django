from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import CartItem, Cart

@receiver(post_save, sender=CartItem)
@receiver(post_delete, sender=CartItem)
def update_cart_total(sender, instance, **kwargs):
    cart = instance.cart
    cart.save()  # This will trigger the Cart's save method to recalculate the total
