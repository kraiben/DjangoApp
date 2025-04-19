
from django.urls import path

from .views import (
    BookListView, BookCreateView, BookUpdateView, BookDeleteView,
    register_view, login_view, logout_view
)

urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('create/', BookCreateView.as_view(), name='book_create'),
    path('update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
]