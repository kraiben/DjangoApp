from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Books
from .forms import BookForm, RegisterForm, LoginForm
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views import View

class BookListView(View):
    def get(self, request):
        books_list = Books.objects.all().order_by('pk')
        paginator = Paginator(books_list, 3)
        page_number = request.GET.get('page', 1)
        books = paginator.get_page(page_number)
        return render(request, 'book_list.html', {
            'books': books,
            'current_page': page_number
        })

@method_decorator(login_required, name='dispatch')
class BookCreateView(View):
    def get(self, request):
        form = BookForm()
        return render(request, 'book_create.html', {'form': form})

    def post(self, request):
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            cnt = Books.objects.count()
            page = (cnt - 1) // 3 + 1
            return redirect(f"{reverse('book_list')}?page={page}")
        return render(request, 'book_create.html', {'form': form})

@method_decorator(user_passes_test(lambda u: u.is_admin()), name='dispatch')
class BookUpdateView(View):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        form = BookForm(instance=book)
        return render(request, 'book_update.html', {
            'form': form,
            'current_page': request.GET.get('page', 1)
        })

    def post(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect(f"{reverse('book_list')}?page={request.GET.get('page', 1)}")
        return render(request, 'book_update.html', {
            'form': form,
            'current_page': request.GET.get('page', 1)
        })

@method_decorator(user_passes_test(lambda u: u.is_admin()), name='dispatch')
class BookDeleteView(View):
    def get(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        return render(request, 'book_confirm_delete.html', {
            'book': book,
            'current_page': request.GET.get('page', 1)
        })

    def post(self, request, pk):
        book = get_object_or_404(Books, pk=pk)
        book.delete()
        return redirect(f"{reverse('book_list')}?page={request.GET.get('page', 1)}")

def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book_list')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('book_list')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('book_list')