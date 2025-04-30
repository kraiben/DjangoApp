from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from .models import Books, Cart, CartItem, Order, OrderItem
from .forms import BookForm, RegisterForm, LoginForm, UserProfileForm, CartItemForm
from django.core.paginator import Paginator
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator
from django.views import View
from django.contrib import messages

@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Ваш профиль успешно обновлен!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'profile.html', {'form': form})

@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        book=book,
        defaults={'quantity': 1}
    )
    
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    
    messages.success(request, f'Книга "{book.name}" добавлена в корзину')
    return redirect('book_list')

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    total_price = cart.total_price()
    
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Товар удален из корзины')
    return redirect('cart')

@login_required
def create_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    cart_items = cart.cartitem_set.all()
    
    if not cart_items:
        messages.warning(request, 'Ваша корзина пуста')
        return redirect('cart')
    
    total_price = cart.total_price()
    order = Order.objects.create(user=request.user, total_price=total_price)
    
    for item in cart_items:
        OrderItem.objects.create(
            order=order,
            book=item.book,
            quantity=item.quantity,
            price=item.book.price
        )
    
    cart_items.delete()
    messages.success(request, 'Ваш заказ успешно оформлен!')
    return redirect('orders')

@login_required
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'orders.html', {'orders': orders})

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