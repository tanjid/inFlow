from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Product)
admin.site.register(ProductBrand)
admin.site.register(ProductCategory)
admin.site.register(LowStock)
admin.site.register(StockIn)