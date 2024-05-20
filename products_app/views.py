from django.shortcuts import render

# Create your views here.
from .models import Product, Category, ProductSizeQuantity
from django.db.models import Sum

def category_all(request):
    '''Отображение всех категорий'''
    categories = Category.objects.all() # получение всех категорий
    return render(request, 'category_all.html', {'categories': categories}) # передача данных в шаблон

def product_category(request, category):
    '''Отображение товаров по категориям'''
    products = Product.objects.filter(category__name=category) # получение товаров по категории
    for product in products:
        product.quantity = ProductSizeQuantity.objects.filter(product=product).aggregate(Sum('quantity'))['quantity__sum'] or 0
    return render(request, 'product_category.html', {'products': products}) # передача данных в шаблон

def product_info(request, product_id):
    '''Отображение информации о товаре'''
    product = Product.objects.get(pk=product_id) # получение товара по id
    productSizeQuantity = ProductSizeQuantity.objects.filter(product=product, quantity__gt=0) # получение размеров и количества товара
    category = product.category.name
    return render(request, 'product_info.html', {'product': product, 'productSizeQuantity': productSizeQuantity, 'category': category}) # передача данных в шаблон
