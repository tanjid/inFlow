

from django import forms
from django.forms import CheckboxInput
from django.forms import ModelForm
from .models import Employee, EmployeePermission
class SignInForm(forms.Form):
    username = forms.CharField(max_length=20)
    password = forms.CharField(widget=forms.PasswordInput())

class EmployeeEditForm(ModelForm):
    class Meta:
        model = Employee
        exclude = ['current_salary', 'current_advance', 'causal_leave', 'user']

        widgets = {
            
        }

class EmployeePermissionEditForm(ModelForm):
    class Meta:
        model = EmployeePermission
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-check-input'