from django.contrib import admin
from .models import MenuItem, CartItem, Order

admin.site.register(MenuItem)
admin.site.register(CartItem)
admin.site.register(Order)

# Register your models here.
