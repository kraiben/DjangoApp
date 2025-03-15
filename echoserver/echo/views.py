from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# def homePageView(request):
#     return HttpResponse("Hello World!")

from django.shortcuts import render, get_object_or_404, redirect
from .models import Books
from .forms import BookForm
from django.core.paginator import Paginator

def book_list(request):
    books_list = Books.objects.all()
    paginator = Paginator(books_list, 3)  # 10 элементов на странице
    page_number = request.GET.get('page')
    books = paginator.get_page(page_number)
    return render(request, 'book_list.html', {'books': books})
    # books = Books.objects.all()
    # return render(request, 'book_list.html', {'books': books})

def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_form.html', {'form': form})

def book_update(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_form.html', {'form': form})

def book_delete(request, pk):
    book = get_object_or_404(Books, pk=pk)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_confirm_delete.html', {'book': book})