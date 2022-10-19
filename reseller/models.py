from email.policy import default
from django.db import models
from products.models import Product

# Create your models here.

class Reseller(models.Model):
    name = models.CharField(max_length= 15)
    number = models.CharField(max_length= 15, null=True, blank=True)
    discount = models.IntegerField()
    address = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name


class ResellerOrder(models.Model):
    date = models.DateField(auto_now_add=True)
    reseller_name = models.ForeignKey(Reseller, on_delete=models.CASCADE)
    sub_total = models.IntegerField(default=0)
    additional_discount = models.IntegerField(default=0, null=True, blank=True)
    grand_total = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.id

class ResellerOrderDetails(models.Model):
    main_order = models.ForeignKey(ResellerOrder, on_delete=models.CASCADE, null=True, blank=True,)
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