from django import forms
from .models import Books, User, CartItem
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm


class BookForm(forms.ModelForm):
    class Meta:
        model = Books
        fields = ['name', 'author', 'price']
        
class RegisterForm(UserCreationForm):
    email = forms.EmailField()
    user_name = forms.CharField(max_length=100, label='User Name')
    
    class Meta:
        model = User
        fields = ['username', 'email', 'user_name', 'password1', 'password2']
        labels = {
            'username': 'Login',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].label = 'Login'
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter your login'})
        self.fields['user_name'].widget.attrs.update({'placeholder': 'Enter your name'})


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label='Логин',
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите ваш логин',
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите ваш пароль',
            'class': 'form-control'
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'user_name']
        labels = {
            'username': 'Логин',
            'email': 'Email',
            'first_name': 'Имя'
        }

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['quantity']
        widgets = {
            'quantity': forms.NumberInput(attrs={
                'min': 1,
                'value': 1,
                'class': 'form-control',
                'style': 'width: 60px;'
            })
        }