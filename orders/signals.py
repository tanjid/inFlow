# from django.dispatch import receiver
# from django.contrib.auth.models import User
# from django.db.models.signals import pre_delete, post_save
# from employees.models import Employee, EmployeePermission, EmplpyeePoints
# from sites.models import Company

# @receiver(pre_delete, sender=OrderDetails)
# def increment_stock(sender, instance, **kwargs):
#     print("Increment Stock Qty using signal")
#     selected_product = Product.objects.get(sku = instance.sku)
#     selected_product.stock_qty += int(instance.qty)
#     selected_product.save()


# @receiver(post_save, sender=User)
# def decrement_stock(sender,created, instance, **kwargs):
#     if created:
#         Employee.objects.create(
#             user = instance,
#             name = instance.first_name,

#         )



