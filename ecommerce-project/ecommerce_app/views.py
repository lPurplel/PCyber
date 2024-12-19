from django.shortcuts import render, HttpResponse, redirect, \
    get_object_or_404, reverse
from django.contrib import messages
from .models import Product, Order, LineItem, Category
from .forms import *
from django.contrib.auth import login, logout
from . import cart



# главная страница
def index(request):
    all_products = Product.objects.all()
    return render(request, "ecommerce_app/index.html", {
                                    'all_products': all_products,
                                    })


# информация товара
def show_product(request, product_id, product_slug):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        form = CartForm(request, request.POST)
        if form.is_valid():
            request.form_data = form.cleaned_data
            cart.add_item_to_cart(request)
            return redirect('show_cart')

    form = CartForm(request, initial={'product_id': product.id})
    return render(request, 'ecommerce_app/product_detail.html', {
                                            'product': product,
                                            'form': form,
                                            })


# все категории
def all_categories(request):
    categories = Category.objects.all()
    return render(request, "ecommerce_app/categories.html", {
        'categories': categories
    })

# товары по категориям
def products_by_category(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, "ecommerce_app/products_by_category.html", {
        'category': category,
        'products': products
    })


# корзина
def show_cart(request):

    if request.method == 'POST':
        if request.POST.get('submit') == 'Изменить':
            cart.update_item(request)
        if request.POST.get('submit') == 'Удалить':
            cart.remove_item(request)

    cart_items = cart.get_all_cart_items(request)
    cart_subtotal = cart.subtotal(request)
    return render(request, 'ecommerce_app/cart.html', {
                                            'cart_items': cart_items,
                                            'cart_subtotal': cart_subtotal,
                                            })


# оформление заказа
def checkout(request):
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            cleaned_data = form.cleaned_data
            o = Order(
                name = cleaned_data.get('name'),
                email = cleaned_data.get('email'),
                phone = cleaned_data.get('phone'),
                address = cleaned_data.get('address'),
            )
            o.save()

            all_items = cart.get_all_cart_items(request)
            for cart_item in all_items:
                li = LineItem(
                    product_id = cart_item.product_id,
                    price = cart_item.price,
                    quantity = cart_item.quantity,
                    order_id = o.id
                )

                li.save()

            cart.clear(request)

            request.session['order_id'] = o.id

            return redirect('success_order')


    else:
        form = CheckoutForm()
        return render(request, 'ecommerce_app/checkout.html', {'form': form})


# сообщение оформленного заказа
def success_order(request):
    return render(request, 'ecommerce_app/success.html')

# регистрация
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login_view')
    else:
        form = SignUpForm()
    return render(request, 'ecommerce_app/register.html', {'form': form})



# авторизация
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
    else:
        form = LoginForm()
    return render(request, 'ecommerce_app/login.html', {'form': form})

# выход
def logout_view(request):
    logout(request)
    return redirect('index')