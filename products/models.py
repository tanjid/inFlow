

# Create your models here.
from django.db import models
from employees.models import Employee

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=20, unique = True)

    def __str__(self):
        return str(self.name)

class ProductBrand(models.Model):
    name = models.CharField(max_length=20, unique = True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique = True)
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.DO_NOTHING, null=True, blank=True)
    warranty = models.CharField(max_length=20)
    warranty_policy = models.TextField(null=True, blank=True)
    cost_price = models.IntegerField()
    sell_price = models.IntegerField()
    alert_qty = models.IntegerField()
    stock_qty = models.IntegerField(null=True, blank=True, default=0)
    product_image = models.ImageField(null=True, blank=True, default="default.jpg", upload_to='products/')

    def __str__(self):
        return str(self.sku)

    def decrese_stock(self, qty):
        self.stock_qty -= qty
        self.save()
    def increse_stock(self, qty):
        self.stock_qty += qty
        self.save()


class AdjustStock(models.Model):
    sku = models.ForeignKey(Product, on_delete=models.RESTRICT)
    qty = models.IntegerField()
    cause = models.CharField(max_length=20)
    note = models.TextField(null=True, blank=True)
    by = models.ForeignKey(Employee, on_delete=models.RESTRICT, null=True, blank=True)