from django.contrib import admin
from .models import Order, CartList

# Register your models here.
admin.site.register(Order)
admin.site.register(CartList)