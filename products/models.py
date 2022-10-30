
# Create your models here.

from django.db import models
from employees.models import Employee


# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=20, unique = True,db_index=True)

    def __str__(self):
        return str(self.name)

class ProductBrand(models.Model):
    name = models.CharField(max_length=20, unique = True, db_index=True)

    def __str__(self):
        return str(self.name)

class Product(models.Model):
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=20, unique = True,db_index=True)
    category = models.ForeignKey(ProductCategory, on_delete=models.DO_NOTHING, null=True, blank=True)
    brand = models.ForeignKey(ProductBrand, on_delete=models.DO_NOTHING, null=True, blank=True)
    warranty = models.CharField(max_length=20, null=True, blank=True)
    warranty_policy = models.TextField(null=True, blank=True)
    cost_price = models.IntegerField()
    sell_price = models.IntegerField()
    alert_qty = models.IntegerField()
    stock_qty = models.IntegerField(null=True, blank=True, default=0)
    product_image = models.ImageField(null=True, blank=True, default="default.jpg", upload_to='products/')
    current_stock_status = models.BooleanField(default=True)

    def __str__(self):
        return str(self.sku)


    def decrese_stock(self, qty):
        self.stock_qty -= qty
        self.save()

        # Check for stock notification

        if self.stock_qty <= self.alert_qty:
            try:
                LowStock.objects.get(sku=self)
            except:
                LowStock.objects.create(
                    sku = self
                )

            try:
                stock_object = StockIn.objects.get(sku=self)
                stock_object.status = False
                stock_object.save()
            except:
                StockIn.objects.create(
                    sku=self
                )

            if self.current_stock_status:
                stock_object = LowStock.objects.get(sku=self)
                stock_object.website = False
                stock_object.mkt = False
                stock_object.active = True
                stock_object.save()


    def increse_stock(self, qty):
        self.stock_qty += qty
        self.save()

        if self.stock_qty > self.alert_qty:
            try:
                low_object = LowStock.objects.get(sku=self)
                low_object.mkt = False
                low_object.website = False
                low_object.active = False
                low_object.save()

            except:
                pass

        try:
            stock_object = StockIn.objects.get(sku=self)
        except:
                StockIn.objects.create(
                    sku=self
                )
        
        if self.stock_qty > 10 and self.current_stock_status == False:
            stock_object.mkt = False
            stock_object.website = False
            stock_object.active = True
            stock_object.save()


class AdjustStock(models.Model):
    sku = models.ForeignKey(Product, on_delete=models.RESTRICT)
    qty = models.IntegerField()
    cause = models.CharField(max_length=20)
    note = models.TextField(null=True, blank=True)
    by = models.ForeignKey(Employee, on_delete=models.RESTRICT, null=True, blank=True)


class LowStock(models.Model):
    sku = models.OneToOneField(Product, on_delete=models.RESTRICT, unique = True, db_index=True)
    website = models.BooleanField(default=False) 
    mkt = models.BooleanField(default=False)
    active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.sku)

class StockIn(models.Model):
    sku = models.OneToOneField(Product, on_delete=models.RESTRICT, unique = True, db_index=True)
    website = models.BooleanField(default=False) 
    mkt = models.BooleanField(default=False)
    active = models.BooleanField(default=True)


    def __str__(self):
        return str(self.sku)