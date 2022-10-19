from email.policy import default
from enum import unique
from django.db import models
from products.models import Product
from employees.models import Employee
from sites.models import Company

class MktShop(models.Model):
    name = models.CharField(max_length=20, unique = True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

class MktOrder(models.Model):
    invoice = models.CharField(max_length=15, null=True, blank=True, unique=True, db_index=True)
    shop_name = models.ForeignKey(MktShop, on_delete=models.RESTRICT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
    update_at = models.DateTimeField(null=True, blank=True,)
    sub_total = models.IntegerField(null=True, blank=True,)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT,null=True, blank=True,)
    # items = models.ManyToManyField(OrderDetails,blank=True,)

    def __str__(self):
        return str(self.invoice)



class MktOrderDetails(models.Model):
    main_order = models.ForeignKey(MktOrder, on_delete=models.CASCADE, null=True, blank=True,)
    Initial = 'Initial'
    Shipping = 'Shipping'
    Complete = 'Complete'  
    Return = 'Return'
    STATUS = [
        (Initial, 'Initial'),
        (Shipping, 'Shipping'),
        (Return, 'Return'),
        (Complete, 'Complete'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS,
        default=Initial,
        
    )
    sku = models.ForeignKey(Product, on_delete=models.RESTRICT)
    qty = models.IntegerField()
    product_prices = models.IntegerField(null=True, blank=True)
    item_totals = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}: {self.sku}"

