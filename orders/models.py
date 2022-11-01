from django.db import models
from products.models import Product
from employees.models import Employee
from sites.models import Company
from django.contrib import messages
# Create your models here.
class DeliveryMethod(models.Model):
    name = models.CharField(max_length=20, unique = True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return str(self.name)

class NewOrder(models.Model):
    mobille_number = models.CharField(max_length=15)
    name = models.CharField(max_length=15)
    delivery_method = models.ForeignKey(DeliveryMethod, on_delete=models.RESTRICT, null=True, blank=True)
    note = models.TextField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    return_note = models.TextField(null=True, blank=True)
    cancel_note = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
    update_at = models.DateTimeField(null=True, blank=True,)
    sub_total = models.IntegerField(null=True, blank=True,)
    advance = models.IntegerField(null=True, blank=True,)
    discount = models.IntegerField(null=True, blank=True,)
    delivery_charge = models.IntegerField(null=True, blank=True,)
    total_price = models.IntegerField(null=True, blank=True,)
    invoice_number = models.CharField(max_length=50, null=True, blank=True, unique=True)
    employee = models.ForeignKey(Employee, on_delete=models.RESTRICT,null=True, blank=True,)
    company = models.ForeignKey(Company, on_delete=models.RESTRICT,null=True, blank=True,)
    is_active = models.BooleanField(default=False)
    in_review = models.BooleanField(default=False)
    # items = models.ManyToManyField(OrderDetails,blank=True,)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return str(self.invoice_number)

    def decide_review_status(self):
        if self.advance > 0:
            self.in_review = True
            self.save()
        if self.discount > self.total_price * .05:
            self.in_review = True
            self.save()



class OrderDetails(models.Model):
    main_order = models.ForeignKey(NewOrder, on_delete=models.CASCADE, null=True, blank=True,)
    Initial = 'Initial'
    Printed = 'Printed'
    Shipping = 'Shipping'
    Complete = 'Complete'  
    Return = 'Return'
    Exchange = 'Exchange'
    Cancel = 'Cancel'
    STATUS = [
        (Initial, 'Initial'),
        (Printed, 'Printed'),
        (Shipping, 'Shipping'),
        (Return, 'Return'),
        (Complete, 'Complete'),
        (Exchange, 'Exchange'),
        (Cancel, 'Cancel'),
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

    # def save(self, *args, **kwargs):

    #     print("from save Deducting Stock from Products")
    #     selected_product = Product.objects.get(sku = self.sku)
    #     selected_product.stock_qty -= int(self.qty)
    #     selected_product.save()
    
    #     super(OrderDetails, self).save(*args, **kwargs)

