from django.shortcuts import render

# Create your views here.
from django.http import JsonResponse
from .services import generate_product_embeddings, recommend_products_for_user
from .models import User, Purchase

from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import User, Product, Purchase
from .forms import UserForm, ProductForm, PurchaseForm
from django.http import HttpResponseRedirect, Http404
from collections import Counter

def get_purchase_history():
    purchases = Purchase.objects.select_related('user', 'product')
    data = [{'user': p.user.name, 'product': p.product.name} for p in purchases]
    return pd.DataFrame(data)

def create_user_item_matrix(data):
    return data.pivot_table(index='user', columns='product', aggfunc='size', fill_value=0)


def recommend_view(request, user_id):
    user = User.objects.get(id=user_id)
    purchase_history = get_purchase_history()
    user_item_matrix = create_user_item_matrix(purchase_history)

    products, embeddings = generate_product_embeddings()
    recommendations = recommend_products_for_user(user.name, user_item_matrix, embeddings)

    response = [{'name': p.name, 'description': p.description} for p in recommendations]
    return JsonResponse(response, safe=False)




# User Management Views
class UserListView(ListView):
    model = User
    template_name = 'recommendation_v2/user_list.html'
    context_object_name = 'users'


class UserCreateView(CreateView):
    model = User
    form_class = UserForm
    template_name = 'recommendation_v2/form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('recommendation_v2:user_list')
    form_title = 'Add User'
    redirect_url = 'recommendation_v2:user_list'


class UserUpdateView(UpdateView):
    model = User
    form_class = UserForm
    template_name = 'recommendation_v2/form.html'
    context_object_name = 'user'
    success_url = reverse_lazy('recommendation_v2:user_list')
    form_title = 'Edit User'
    redirect_url = 'recommendation_v2:user_list'


class UserDeleteView(DeleteView):
    model = User
    template_name = 'recommendation_v2/confirm_delete.html'
    success_url = reverse_lazy('recommendation_v2:user_list')


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'user'
        context['redirect_url'] = 'recommendation_v2:user_list'
        return context

# Product Management Views
class ProductListView(ListView):
    model = Product
    template_name = 'recommendation_v2/product_list.html'
    context_object_name = 'products'


class ProductCreateView(CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'recommendation_v2/form.html'
    context_object_name = 'product'
    success_url = reverse_lazy('recommendation_v2:product_list')
    form_title = 'Add Product'
    redirect_url = 'recommendation_v2:product_list'


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'recommendation_v2/form.html'
    context_object_name = 'product'
    success_url = reverse_lazy('recommendation_v2:product_list')
    form_title = 'Edit Product'
    redirect_url = 'recommendation_v2:product_list'


class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'recommendation_v2/confirm_delete.html'
    success_url = reverse_lazy('recommendation_v2:product_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'product'
        context['redirect_url'] = 'recommendation_v2:product_list'
        return context

# Purchase Management Views
class PurchaseListView(ListView):
    model = Purchase
    template_name = 'recommendation_v2/purchase_list.html'
    context_object_name = 'purchases'


class PurchaseCreateView(CreateView):
    model = Purchase
    form_class = PurchaseForm
    template_name = 'recommendation_v2/form.html'
    context_object_name = 'purchase'
    success_url = reverse_lazy('recommendation_v2:purchase_list')
    form_title = 'Add Purchase'
    redirect_url = 'recommendation_v2:purchase_list'


class PurchaseDeleteView(DeleteView):
    model = Purchase
    template_name = 'recommendation_v2/confirm_delete.html'
    success_url = reverse_lazy('recommendation_v2:purchase_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object_name'] = 'purchase'
        context['redirect_url'] = 'recommendation_v2:purchase_list'
        return context



class RecommendationsView(ListView):
    model = Product
    template_name = 'recommendation_v2/recommendations.html'
    context_object_name = 'recommendations'

    def get_queryset(self):
        # Retrieve the user using the pk passed from the URL
        user = get_object_or_404(User, pk=self.kwargs['pk'])

        # Get the list of products purchased by the user
        purchased_products = Purchase.objects.filter(user=user).values_list('product', flat=True)

        # Recommend products not already purchased by the user
        recommendations = Product.objects.exclude(id__in=purchased_products)[:10]

        return recommendations

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the user to the context so it can be used in the template
        user = get_object_or_404(User, pk=self.kwargs['pk'])
        context['user'] = user
        return context




