from django.contrib import admin
from .models import Category, Product, Brand, ProductSize, ProductSizeQuantity

@admin.action(description='Сбросить кол. товара на 0')
def reset_quantity(modeladmin, request, queryset):
    queryset.update(quantity=0)

class ProductSizeQuantityInline(admin.TabularInline):  # Inline модель, которая позволяет редактировать связанные модели на одной странице
    model = ProductSizeQuantity # модель, которую вы хотите редактировать
    extra = 1 # количество дополнительных форм для ввода

class ProductAdmin(admin.ModelAdmin):
    actions = [reset_quantity]
    list_display = ('name', 'category', 'brand', 'price', 'delivery_price', 'date_added', 'rating', 'active')
    list_filter = ('category', 'brand', 'date_added', 'rating', 'active', 'delivery_price')
    search_fields = ('name', 'description')
    list_editable = ('price', 'active', 'delivery_price')
    readonly_fields = ['date_added', 'rating']
    fieldsets = [
        (None, {
            'classes': ['wide'],
            'fields': ['name', 'image', 'product_weight', 'delivery_time']
        }),
        ('Категория товара и его подробное описание', {
            'classes': ['collapse'],
            'fields': ['category', 'brand', 'description'],
        }),
        ('Цена', {
            'fields': ['price', 'delivery_price']
        }),
        ('Рейтинг и прочее', {
            'fields': ['date_added', 'rating', 'active'],
        }),
    ]
    inlines = [ProductSizeQuantityInline]  # добавление Inline модели (размер и количество товара)

class ProductSizeAdmin(admin.ModelAdmin):
    list_display = ('size', 'category')
    list_editable = ('category',)





'''Регистрации моделей в админке'''
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Brand)
admin.site.register(ProductSize, ProductSizeAdmin)

