from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from sites.models import Company
import random
from datetime import datetime
# Create your models here.



class Employee(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='employes', null=True, blank=True)
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
    # points = models.ForeignKey(EmplpyeePoints, on_delete=models.RESTRICT, null=True, blank=True)

    

    def __str__(self):
        return self.name

    def get_invoice_number(self):
        invoive_slug = self.assigned_company.invoice_slug
        invoive_id = self.assigned_company.invoice_count
        self.assigned_company.invoice_count += 1
        random_num1 =  random.randint(0, 9)
        random_num2 =  random.randint(0, 9)
        inovice_int = f'{random_num1}{invoive_id}{random_num2}'
        numbers = [ str(x) for x in inovice_int ]
        random.shuffle(numbers)
        shu_invoice = "".join(numbers)
        inovice = f"{invoive_slug}{shu_invoice}"



        self.assigned_company.save()
        return inovice

    def add_points(self, field):
        now = datetime.now()
        current_hour = int(now.strftime('%H'))
        today = datetime.today().date()
        employee = self
        obj = EmplpyeePoints.objects.filter(employee=employee, created__date = today, created__hour = current_hour)
        if obj.exists():
            
            em = obj[0]
            if field == "new_order":
                em.new_order += 1
            elif field == "complete_order":
                em.complete_order += 1
            elif field == "return_order":
                em.return_order += 1
            elif field == "ad_note":
                em.ad_note += 1
            elif field == "rtn_note":
                em.rtn_note += 1
            elif field == "search":
                em.search += 1
            elif field == "misc":
                em.misc += 1
                
            em.save()

        else:
            if field == "new_order":
                EmplpyeePoints.objects.create(
                    employee=employee,
                    new_order = 1

                )
            elif field == "complete_order":
                EmplpyeePoints.objects.create(
                    employee=employee,
                    complete_order = 1

                )
            elif field == "return_order":
                EmplpyeePoints.objects.create(
                    employee=employee,
                    return_order = 1

                )
            elif field == "ad_note":
                EmplpyeePoints.objects.create(
                    employee=employee,
                    ad_note = 1

                )
            elif field == "rtn_note":
                EmplpyeePoints.objects.create(
                    employee=employee,
                    rtn_note = 1

                )
            elif field == "search":
                EmplpyeePoints.objects.create(
                    employee=employee,
                    search = 1

                )
            elif field == "misc":
                EmplpyeePoints.objects.create(
                    employee=employee,
                    misc = 1

                )

# class EmplyeeParentAcc(models.Model):
#     name = models.CharField(max_length=30)
#     employee = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True, blank=True)
#     is_parent = models.BooleanField(default=False)

#     def __str__(self):
#         return str(self.name)

class EmplpyeePoints(models.Model):
    employee = models.ForeignKey(Employee, on_delete = models.CASCADE, null=True, blank=True)
    # name = models.CharField(max_length=50, default="admin")
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True,)
    total = models.IntegerField(default=0)
    new_order = models.IntegerField(default=0)
    complete_order = models.IntegerField(default=0)
    return_order = models.IntegerField(default=0)
    ad_note = models.IntegerField(default=0)
    rtn_note = models.IntegerField(default=0)
    search = models.IntegerField(default=0)
    misc = models.IntegerField(default=0)
    def save(self, *args, **kwargs):
        self.total = (self.new_order * 10) + (self.complete_order *2) + (self.return_order *3)  + (self.ad_note * 6) + (self.rtn_note * 6) + self.search + self.misc
        super(EmplpyeePoints, self).save(*args, **kwargs)


        # if field == "new_order":
        #     self.new_order += 1
        #     self.save()

    def __str__(self):
        return str(f"{self.employee} : {self.created.hour + 6}")

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
    edit_order = models.BooleanField(default=False)
    cancel_order = models.BooleanField(default=False)
    exchange_order = models.BooleanField(default=False)
    return_order = models.BooleanField(default=False)
    confirm_order = models.BooleanField(default=False)
    print_order = models.BooleanField(default=False)

    search_confirm = models.BooleanField(default=False)
    search_rtn = models.BooleanField(default=False)

    dashboard = models.BooleanField(default=False)

    order_list = models.BooleanField(default=False)

    employes = models.BooleanField(default=False)

    purchase = models.BooleanField(default=False)

    reports = models.BooleanField(default=False)

    inven = models.BooleanField(default=False)

    reseller = models.BooleanField(default=False)

    mkt = models.BooleanField(default=False)



    def __str__(self):
     return str(self.user)



