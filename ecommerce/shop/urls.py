from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('customers/', views.list_customers, name='customer_list'),
    path('customers/add/', views.create_customer, name='create_customer'),
    path('customers/<int:pk>/edit/', views.update_customer, name='update_customer'),
    path('customers/<int:pk>/delete/', views.delete_customer, name='delete_customer'),

    path('products/', views.list_products, name='product_list'),
    path('products/add/', views.create_product, name='create_product'),
    path('products/<int:pk>/edit/', views.update_product, name='update_product'),
    path('products/<int:pk>/delete/', views.delete_product, name='delete_product'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_detail, name='cart_detail'),


    path('generate-description/', views.generate_description, name='generate_description'),

    path('purchase-history/', views.purchase_history, name='purchase_history'),
    path('purchase-details/<int:purchase_id>/', views.purchase_details, name='purchase_details'),

]
