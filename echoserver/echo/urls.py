from urllib.parse import urlparse
from django.urls import path

from .views import book_create, book_delete, book_list, book_update


urlpatterns = [
    # path("", homePageView, name = 'home')
    path('', book_list, name='book_list'),
    path('create/', book_create, name='book_create'),
    path('update/<int:pk>/', book_update, name='book_update'),
    path('delete/<int:pk>/', book_delete, name='book_delete'),
]