from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from sites.models import Company
import random

# Create your models here.

class EmplpyeePoints(models.Model):
    name = models.CharField(max_length=50, default="admin")
    total = models.IntegerField(default=0)
    new_order = models.IntegerField(default=0)
    complete_order = models.IntegerField(default=0)
    return_order = models.IntegerField(default=0)
    ad_note = models.IntegerField(default=0)
    rtn_note = models.IntegerField(default=0)
    search = models.IntegerField(default=0)
    misc = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        self.total = self.new_order + self.complete_order + self.return_order + self.ad_note + self.rtn_note + self.search + self.misc
        super(EmplpyeePoints, self).save(*args, **kwargs)
    def __str__(self):
        return self.name
class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='employes')
    assigned_company = models.ForeignKey(Company, on_delete = models.CASCADE, null=True, blank=True)
    
    designation = models.CharField(max_length=50, null=True, blank=True)
    blood_group = models.CharField(max_length=50,null=True, blank=True)
    present_address = models.TextField(null=True, blank=True)
    permanent_address = models.TextField(null=True, blank=True)
    official_number = models.CharField(max_length=20, null=True, blank=True)
    personal_number = models.CharField(max_length=20, null=True, blank=True)
    alt_personal_number = models.CharField(max_length=20, null=True, blank=True)
    guardian_number = models.CharField(max_length=20, null=True, blank=True)
    official_email= models.EmailField(null=True, blank=True)
    persoanl_email= models.EmailField(null=True, blank=True)
    current_salary = models.IntegerField(null=True, blank=True)
    current_advance = models.IntegerField(null=True, blank=True)
    causal_leave = models.IntegerField(null=True, blank=True)
    points = models.ForeignKey(EmplpyeePoints, on_delete=models.RESTRICT, null=True, blank=True)

    

    def __str__(self):
        return self.name

    def get_invoice_number(self):
        invoive_slug = self.assigned_company.invoice_slug
        invoive_id = self.assigned_company.invoice_count
        self.assigned_company.invoice_count += 1
        random_num1 =  random.randint(9, 99)
        random_num2 =  random.randint(9, 99)
        inovice_int = f'{random_num1}{invoive_id}{random_num2}'
        numbers = [ str(x) for x in inovice_int ]
        random.shuffle(numbers)
        shu_invoice = "".join(numbers)
        inovice = f"{invoive_slug}{shu_invoice}"



        self.assigned_company.save()
        return inovice


class EmployeePermission(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE, null=True, blank=True)
    order_perm = models.BooleanField(default=True)
    Initial = models.BooleanField(default=False)
    Printed = models.BooleanField(default=False)
    Shipping = models.BooleanField(default=False)
    Complete = models.BooleanField(default=False)
    Return = models.BooleanField(default=False)
    Exchange = models.BooleanField(default=False)
    Cancel = models.BooleanField(default=False)

    def __str__(self):
     return str(self.user)



