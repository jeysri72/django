from django.urls import path
from . import views

app_name = 'recommendation_v2'

urlpatterns = [
    # User management URLs
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/add/', views.UserCreateView.as_view(), name='user_add'),
    path('users/<int:pk>/edit/', views.UserUpdateView.as_view(), name='user_edit'),
    path('users/<int:pk>/delete/', views.UserDeleteView.as_view(), name='user_delete'),

    # Product management URLs
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/add/', views.ProductCreateView.as_view(), name='product_add'),
    path('products/<int:pk>/edit/', views.ProductUpdateView.as_view(), name='product_edit'),
    path('products/<int:pk>/delete/', views.ProductDeleteView.as_view(), name='product_delete'),

    # Purchase management URLs
    path('purchases/', views.PurchaseListView.as_view(), name='purchase_list'),
    path('purchases/add/', views.PurchaseCreateView.as_view(), name='purchase_add'),
    path('purchases/<int:pk>/delete/', views.PurchaseDeleteView.as_view(), name='purchase_delete'),

    # Recommendations URL
    path('recommendations/<int:pk>', views.RecommendationsView.as_view(), name='recommendations'),
]
