from django.shortcuts import render

from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Books
from .forms import BookForm
from django.core.paginator import Paginator


class Views():

    def __init__(self) -> None:
        self.currentPage = 1
        self.books_list = Books.objects.all()
        self.paginator = Paginator(self.books_list, 3)

    def refresh(self):
        self.books_list = Books.objects.all()
        self.paginator = Paginator(self.books_list, 3)

    def book_list(self, request):
        self.refresh()
        page_number = request.GET.get('page')
        if isinstance(page_number, str):
            if page_number.isdigit():
                self.currentPage = int(page_number)
            else:
                self.currentPage = 1
        else:
            self.currentPage = 1
        books = self.paginator.get_page(page_number)
        return render(request, 'book_list.html', {'books': books})

    def book_create(self, request):
        if request.method == 'POST':
            form = BookForm(request.POST)
            if form.is_valid():
                form.save()
                cnt = Books.objects.count()
                page = cnt // 3
                if cnt % 3 != 0:
                    page += 1
                return redirect(f"{reverse('book_list')}?page={page}")
        else:
            form = BookForm()
        return render(request, 'book_create.html', {'form': form, 'page': self.currentPage})

    def book_update(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        print(self.currentPage)
        if request.method == 'POST':
            form = BookForm(request.POST, instance=book)
            if form.is_valid():
                form.save()
                return redirect(f"{reverse('book_list')}?page={self.currentPage}")
        else:
            form = BookForm(instance=book)
        return render(request, 'book_update.html', {'form': form, 'on_page': self.currentPage})

    def book_delete(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        # position = Books.objects.filter(id__lt=book.pk).count() + 1
        # page = position // 3
        # if page % 3 != 0: page += 1
        if request.method == 'POST':
            book.delete()
            return redirect(f"{reverse('book_list')}?page={self.currentPage}")
        return render(request, 'book_confirm_delete.html', {'book': book, 'from_page': self.currentPage})
