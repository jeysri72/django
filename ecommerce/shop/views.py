# Correct way to import timezone in Django:
from django.utils import timezone

from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Customer, Product, Cart, CartItem, PurchaseHeader, PurchaseDetail
from .forms import CustomerForm, ProductForm
from transformers import pipeline
from django.http import JsonResponse

from django.shortcuts import render
import json

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







@csrf_exempt
def add_to_cart(request):
    """View to add a product to the cart."""
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            product_id = data.get('product_id')
            print (product_id)

            # Validate product existence
            product = get_object_or_404(Product, id=product_id)
            print (product)

            customer_id = 1 # Replace with the logged-in user if authentication is implemented
            customer = get_object_or_404(Customer, id=customer_id)
            print(customer)


            # Get or create a cart for the session user
            cart, created = Cart.objects.get_or_create(
                customer = customer,  
                product = product,
                created_at = timezone.now(),
                updated_at = timezone.now(),
                defaults={'discount': 0, 'total': 0}
            )

            # Check if the product is already in the cart
            cart_item, created = CartItem.objects.get_or_create(
                cart=cart,
                product=product,
                defaults={
                    'qty': 1,
                    'price': product.price,
                    'discount': 0,
                    'line_total': product.price
                }
            )

            if not created:
                # If the product is already in the cart, increase the quantity
                cart_item.qty += 1
                cart_item.line_total = cart_item.qty * cart_item.price
                cart_item.save()

            # Recalculate cart total after adding the item
            cart.total = sum(item.line_total for item in cart.cartitem_set.all())
            cart.save()

            return JsonResponse({"success": True})
        except Exception as e:
            return JsonResponse({"error": str(e)}, status=400)

    return JsonResponse({"error": "Invalid request method."}, status=405)


def cart_detail(request):
    """View to display cart details."""
    # Get the cart for the session user
    cart = Cart.objects.prefetch_related('cartitem_set__product').first()  # Replace logic for authenticated users if necessary
    return render(request, 'cart_detail.html', {'cart': cart})




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
