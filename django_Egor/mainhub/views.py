from django import forms
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import TemplateView

from .forms import ProductForm
from .models import Book, Post, Product


def post_list(request):
    posts = Post.objects.all()
    books = Book.objects.all()
    tab = request.GET.get('tab', 'posts')
    return render(request, 'mainhub/post_list.html', {'posts': posts, 'books': books, 'tab': tab})


class HomeView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['message'] = 'Привет, Django (class-based view)!'
        return context


def home_view(request):
    return HomeView.as_view()(request)


@login_required
def home(request):
    context = {
        'name': request.user.username or 'Пользователь',
        'user': request.user,
    }
    return render(request, 'mainhub/post_list.html', context)


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Регистрация прошла успешно.')
            return redirect('post_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=100)
    email = forms.EmailField(label='Email')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            return HttpResponse('Спасибо!')
    else:
        form = ContactForm()
    return render(request, 'contact.html', {'form': form})


def product_list(request):
    products = Product.objects.select_related('category').all()
    return render(request, 'main/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product.objects.select_related('category'), pk=pk)
    return render(request, 'main/product_detail.html', {'product': product})


@login_required
def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        if form.is_valid():
            try:
                product = form.save()
                messages.success(request, f'Товар "{product.name}" создан.')
                return redirect('product_list')
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ProductForm()
    return render(request, 'main/product_form.html', {'form': form})


@login_required
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        if form.is_valid():
            try:
                product = form.save()
                messages.success(request, f'Товар "{product.name}" обновлён.')
                return redirect('product_detail', pk=product.pk)
            except ValidationError as e:
                form.add_error(None, e)
    else:
        form = ProductForm(instance=product)
    return render(request, 'main/product_form.html', {'form': form, 'product': product})


@login_required
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.warning(request, 'Товар удалён.')
        return redirect('product_list')
    return render(request, 'main/product_confirm_delete.html', {'product': product})
