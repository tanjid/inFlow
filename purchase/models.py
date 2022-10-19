from django.db import models
from products.models import Product
# Create your models here.


class PurchaseItems(models.Model):
    sku = models.ForeignKey(Product, on_delete=models.CASCADE)
    qty = models.IntegerField(null=True, blank=True,)
    price = models.IntegerField(null=True, blank=True,)
    sell_price = models.IntegerField(null=True, blank=True,)

    def __str__(self):
        return f"{self.id}: {self.sku}"

class Purchase(models.Model):
    date = models.DateField(auto_now_add=True, null=True, blank=True,)
    purchase_note = models.CharField(max_length=15, null=True, blank=True,)
    items = models.ManyToManyField(PurchaseItems,blank=True,)
    grand_total = models.IntegerField(null=True, blank=True,)

    def __str__(self):
        return f"{self.id} : {self.items}"