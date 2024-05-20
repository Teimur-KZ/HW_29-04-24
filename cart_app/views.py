from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect, get_object_or_404
from .models import Cart, CartProduct
from products_app.models import Product, ProductSize

def add_to_cart(request, product_id):
    '''Добавление товара в корзину'''
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    size = get_object_or_404(ProductSize, pk=request.POST.get('size'))
    cart_product, created = CartProduct.objects.get_or_create(
        cart=cart, product=product, size=size
    )
    cart_product, created = CartProduct.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_product.quantity += 1
        cart_product.save()
    return redirect('cart_view')

def remove_from_cart(request, product_id):
    '''Удаление товара из корзины'''
    product = get_object_or_404(Product, id=product_id)
    CartProduct.objects.filter(cart__user=request.user, product=product).delete()
    return redirect('cart_view')


def change_quantity(request, product_id, quantity):
    '''Изменение количества товара в корзине'''
    cart, created = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, pk=product_id)
    cart_product = get_object_or_404(CartProduct, cart=cart, product=product)

    new_quantity = request.POST.get('quantity')
    if new_quantity:
        cart_product.quantity = int(new_quantity)
        cart_product.save()

    return redirect('cart_view')


def cart_view(request):
    '''Представление для корзины покупок'''
    cart, created = Cart.objects.get_or_create(user=request.user)

    return render(request, 'cart.html', {'cart': cart})

def order_view(request):
    '''Представление для оформления заказа'''
    # добавить логику для оформления заказа
    pass
