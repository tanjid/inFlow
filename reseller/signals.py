from django.dispatch import receiver
from django.db.models.signals import pre_delete, post_save
from products.models import Product
from .models import ResellerOrderDetails

@receiver(pre_delete, sender=ResellerOrderDetails)
def increment_stock(sender, instance, **kwargs):
    print("Increment Stock Qty using signal")
    selected_product = Product.objects.get(sku = instance.sku)
    selected_product.stock_qty += int(instance.qty)
    selected_product.save()


@receiver(post_save, sender=ResellerOrderDetails)
def decrement_stock(sender,created, instance, **kwargs):

    if created:
        print("decrement_stock using signal")
        selected_product = Product.objects.get(sku = instance.sku)
        selected_product.stock_qty -= int(instance.qty)
        selected_product.save()

    else:
        print("not decrement_stock bcause not creted")
