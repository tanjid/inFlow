from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from sites.models import Company
# Create your models here.

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

    

    def __str__(self):
        return self.name

    def get_invoice_number(self):
        invoive_slug = self.assigned_company.invoice_slug
        invoive_id = self.assigned_company.invoice_count
        self.assigned_company.invoice_count += 1
        inovice = f"{invoive_slug}-{invoive_id}"
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

