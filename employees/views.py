from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView
from django.views.generic.edit import CreateView
from _keenthemes.__init__ import KTLayout
from .models import *
from _keenthemes.libs.theme import KTTheme
from .forms import SignInForm
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import EmployeeEditForm, EmployeePermissionEditForm
# Create your views here.


class EmployeePermissionEdit(SuccessMessageMixin, UpdateView):
    template_name = 'employees/employee_permission_edit.html'
    model = EmployeePermission
    success_message = " edited successfully"
    form_class = EmployeePermissionEditForm
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/test.js')
        return context

    def get_success_url(self):
        return reverse('test_message')
    

class EmployeeEdit(SuccessMessageMixin, UpdateView):
    template_name = 'employees/employee_edit.html'
    model = Employee
    success_message = " edited successfully"
    form_class = EmployeeEditForm
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/test.js')
        return context

    def get_success_url(self):
        return reverse('test_message')
    




class EmplyeesHome(CreateView):
    template_name = 'employees/employees_home.html'
    model = Employee
    fields = '__all__'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/test.js')
        


        return context

class LoginView(SuccessMessageMixin, FormMixin, TemplateView):
    template_name = 'employees/login.html'
    form_class = SignInForm
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        # status_list = ['Initial', 'Assigned', 'Pending', 'Complete', 'Return']
       
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(request, username=username, password=password)
            messages.success(self.request, "This is my success message")
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.success(self.request, "This is my wrong message")
            return redirect('index')