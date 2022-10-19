from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(NewOrder)
admin.site.register(OrderDetails)
admin.site.register(DeliveryMethod)
