# Correct way to import timezone in Django:
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Customer, Product, Cart, CartItem, PurchaseHeader, PurchaseDetail, Feedback
from .forms import CustomerForm, ProductForm, FeedbackForm, CartItemForm
from transformers import pipeline
from django.http import JsonResponse

from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

import json
import nltk
nltk.download('vader_lexicon')
from nltk.sentiment import SentimentIntensityAnalyzer
# When to use vader?
# •	Social media sentiment analysis (e.g., tweets, reviews, or comments).
# •	Short texts where emojis, slang, and punctuation are common.
# •	When speed and simplicity are priorities over advanced machine learning models.



def home(request):
    """
    View function to render the home page.

    Args:
        request: The HTTP request object.

    Returns:
        Rendered home.html template with context (if needed).
    """
    # If you need to pass context data, you can define it here
    context = {
        'page_title': 'Home Page',  # Example context data
    }
    return render(request, 'home.html', context)

# Create a customer
def create_customer(request):
    if request.method == "POST":
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customer_form.html', {'form': form})

# List customers
def list_customers(request):
    customers = Customer.objects.all()
    return render(request, 'customer_list.html', {'customers': customers})

# Update a customer
def update_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customer_form.html', {'form': form})

# Delete a customer
def delete_customer(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == "POST":
        customer.delete()
        return redirect('customer_list')
    return render(request, 'customer_confirm_delete.html', {'customer': customer})


# GenAI model for description generation
def generate_product_description(name):
    generator = pipeline('text-generation', model='gpt2')
    prompt = f"Write a product description for {name}:"
    result = generator(prompt, max_length=50, num_return_sequences=1)
    return result[0]['generated_text']




def generate_description(request):
    if request.method == "POST":
        prompt = request.POST.get('prompt', '')
        if not prompt:
            return JsonResponse({"error": "Prompt is required."}, status=400)
        
        # Generate the description (replace with your own logic)
        generator = pipeline('text-generation', model='gpt2')
        result = generator(prompt, max_length=50, num_return_sequences=1)
        generated_description = result[0]['generated_text']
        return JsonResponse({"description": generated_description})
    
    return JsonResponse({"error": "Invalid request method."}, status=405)


# Create a product with dynamic description
def create_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            product = form.save(commit=False)
            # Access the 'prompt' field value for additional logic
            # prompt_value = form.cleaned_data.get('prompt')
            # product.description = generate_product_description(prompt_value)
            product.save()
            return redirect('product_list')
    else:
        form = ProductForm()
    return render(request, 'product_form.html', {'form': form})

# List products
def list_products(request):
    # products = Product.objects.all()
    # return render(request, 'product_list.html', {'products': products})

    query = request.GET.get('query', '')
    products = Product.objects.all()
    if query:
        products = products.filter(description__icontains=query)
    return render(request, 'product_list.html', {'products': products})

# Update a product
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    return render(request, 'product_form.html', {'form': form})

# Delete a product
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == "POST":
        product.delete()
        return redirect('product_list')
    return render(request, 'product_confirm_delete.html', {'product': product})



def purchase_history(request):
    """View to display the purchase history of the logged-in customer."""
    customer = request.user.customer  # Assuming a one-to-one relationship with User
    purchase_headers = PurchaseHeader.objects.filter(customer=customer).order_by('-purchase_date')
    context = {
        'purchase_headers': purchase_headers,
    }
    return render(request, 'purchase_history.html', context)

def purchase_details(request, purchase_id):
    """View to display the details of a specific purchase."""
    purchase_header = get_object_or_404(PurchaseHeader, id=purchase_id, customer=request.user.customer)
    purchase_details = PurchaseDetail.objects.filter(purchaseHeader=purchase_header)
    context = {
        'purchase_header': purchase_header,
        'purchase_details': purchase_details,
    }
    return render(request, 'purchase_details.html', context)




# View to display the cart and its item

@login_required
def cart_detail(request):
    """View to display cart details."""
    # Get the cart for the session user
    cart_customer = Customer.objects.get(email=request.user.email)
    cart = Cart.objects.get(customer=cart_customer)
    cart_items = cart.items.all()
    print("cart ")
    print(cart)
    print (cart_items)
    if not cart:
        messages.error(request, "You don't have a cart.")
        return redirect('product_list')  # Redirect to product list if no cart exists
    return render(request, 'cart_detail.html', {'cart': cart, 'cart_items': cart_items})

# View to add a product to the cart 
@login_required
def add_to_cart(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            print(product_id)

            customer_email = request.user.email
            print(customer_email)

            cart_customer = Customer.objects.get(email=customer_email)
            print(cart_customer)

            product = get_object_or_404(Product, id=product_id)
            print(product)

            cart, created = Cart.objects.get_or_create(
                customer=cart_customer,
                defaults={'discount': 0, 'total': 0}
            )

            # Set timestamps if the cart is newly created or updated
            cart.updated_at = timezone.now()
            if created:
                cart.created_at = timezone.now()
            cart.save()

            print(cart)

            # Check if the product is already in the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={'qty': 1, 'price': product.price, 'discount': 0}
            )

            if not created:
                # If already in cart, just increase quantity
                cart_item.qty += 1
                cart_item.save()

            # Recalculate the cart total and discount
            cart_items = CartItem.objects.filter(cart=cart)
            total = 0
            discount = 0

            for item in cart_items:
                item_total = item.price * item.qty
                total += item_total
                discount += item.discount  # Update this if specific discount logic applies per item

            cart.total = total
            cart.discount = discount  # Update this if you apply global cart-level discounts
            cart.save()

            return JsonResponse({"success": True, "total": cart.total, "discount": cart.discount})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)




#View to edit a product quantity in the cart
@login_required
def edit_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)

    if request.method == 'POST':
        form = CartItemForm(request.POST, instance=cart_item)
        if form.is_valid():
            form.save()  # Save the updated quantity and line total
            cart_item.cart.save()  # Recalculate the cart total
            messages.success(request, 'Cart item updated successfully!')
            return redirect('cart_detail')
        else:
            messages.error(request, 'Invalid form submission. Please try again.')

    else:
        form = CartItemForm(instance=cart_item)
    
    return render(request, 'edit_cart_item.html', {'form': form})

# View to delete a product from the cart
@login_required
def delete_cart_item(request, cart_item_id):
    cart_item = get_object_or_404(CartItem, id=cart_item_id)
    cart_item.delete()  # Delete the cart item
    cart_item.cart.save()  # Recalculate the cart total after deletion
    messages.success(request, 'Item removed from cart.')
    return redirect('cart_detail')




def analyze_sentiment(self):
    sia = SentimentIntensityAnalyzer()
    sentiment_scores = sia.polarity_scores(self.comments)
    self.sentiment_score = sentiment_scores['compound']
    if sentiment_scores['compound'] > 0.05:
        self.sentiment = "Positive"
    elif sentiment_scores['compound'] < -0.05:
        self.sentiment = "Negative"
    else:
        self.sentiment = "Neutral"


@login_required
def submit_feedback(request, product_id):
    """View to submit feedback for a product."""
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            customer = Customer.objects.get(email=request.user.email)
            feedback.customer = customer
            feedback.product = product
            analyze_sentiment(feedback)
            feedback.save()
            messages.success(request, "Thank you for your feedback!")
            return redirect('product_list')
    else:
        form = FeedbackForm()

    return render(request, 'submit_feedback.html', {'form': form, 'product': product})


@login_required
def view_feedback(request, product_id):
    """View to see feedback for a specific product."""
    product = get_object_or_404(Product, id=product_id)
    feedback_list = Feedback.objects.filter(product=product).select_related('customer').order_by('-created_at')

    return render(request, 'feedback/view_feedback.html', {
        'product': product,
        'feedback_list': feedback_list,
    })

