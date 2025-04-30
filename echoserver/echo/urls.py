
from django.urls import path

from .views import (
    BookListView, BookCreateView, BookUpdateView, BookDeleteView,
    register_view, login_view, logout_view, profile_view,
    add_to_cart, cart_view, remove_from_cart, create_order, orders_view
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('profile/', profile_view, name='profile'),
    path('add-to-cart/<int:book_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_view, name='cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove_from_cart'),
    path('create-order/', create_order, name='create_order'),
    path('orders/', orders_view, name='orders'),
]