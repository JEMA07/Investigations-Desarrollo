from django.contrib import admin
from .models import MenuItems, Category, Cart, Order, Restaurantes
# Register your models here.
admin.site.register(MenuItems)
admin.site.register(Category)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Restaurantes)
