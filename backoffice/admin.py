from django.contrib import admin

# Register your models here.
from .models import Product, ProductItem
admin.site.register(Product)
admin.site.register(ProductItem)