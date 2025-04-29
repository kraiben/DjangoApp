
from django.urls import path

from .views import (
    BookListView, BookCreateView, BookUpdateView, BookDeleteView,
    register_view, login_view, logout_view, ProfileView, CartView, add_to_cart,
     remove_from_cart, checkout, OrderListView, OrderDetailView
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    
    path('profile/', ProfileView.as_view(), name='profile'),
    path('cart/', CartView.as_view(), name='cart'),
    path('cart/add/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/checkout/', checkout, name='checkout'),
    path('orders/', OrderListView.as_view(), name='order_list'),
    path('orders/<int:order_id>/', OrderDetailView.as_view(), name='order_detail'),
]