from django.db import models

# Create your models here.
from products_app.models import Product, ProductSize


'''Корзина покупок'''

class Cart(models.Model):
    '''Корзина покупок'''
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField('products_app.Product', through='CartProduct', verbose_name='Товары')

    def __str__(self):
        return f'Корзина {self.user.username}'

class CartProduct(models.Model):
    '''Товар в корзине'''
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveSmallIntegerField(default=1, verbose_name='Количество')
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.product.name} в корзине {self.cart.user.username}'

    def get_total(self):
        '''Общая стоимость товара в корзине'''
        return self.product.price * self.quantity


# py manage.py makemigrations cart_app
# py manage.py migrate


