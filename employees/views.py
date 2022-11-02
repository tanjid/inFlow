from django.shortcuts import render
from django.views.generic import TemplateView, UpdateView, ListView
from django.views.generic.edit import CreateView
from _keenthemes.__init__ import KTLayout
from .models import *
from _keenthemes.libs.theme import KTTheme
from .forms import SignInForm, EmployeeCreationForm
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse,reverse_lazy
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from .forms import EmployeeEditForm, EmployeePermissionEditForm
from django.contrib.auth.models import User
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
        em_id = self.kwargs['pk']
        em_permission = EmployeePermission.objects.get(pk=em_id)
        context['em_permission'] = em_permission
        # KTTheme.addJavascriptFile('js/custom/test.js')
        return context

    def get_success_url(self):
        return reverse('employee_permission_edit', kwargs={'pk': self.object.pk})
class EmployeePermissionList(ListView):
    template_name = 'employees/employees_permission_list.html'
    model = EmployeePermission
    
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/test.js')
        return context

    

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
            
        if user is not None:
            login(request, user)
            messages.success(self.request, "logged in seccessfully")
            return redirect('index')
        else:
            messages.success(self.request, "there was an error please try again")
            return redirect('index')


def logout_view(request):
    messages.success(request, "You are logged out.")
    logout(request)
    return redirect('login')

class CreateEmployeeView(SuccessMessageMixin, FormMixin, TemplateView):
    template_name = 'employees/create.html'
    form_class = EmployeeCreationForm
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
            username = form.cleaned_data['user_name']
            name = form.cleaned_data['name']
            password = form.cleaned_data['password']
            company = form.cleaned_data['company']

            if User.objects.filter(username=username).exists():


                messages.INFO(request, "username already exists. Try new one")
                return redirect('create')


            # Creating New user
            new_user = User.objects.create_user(
                username = username,
                password=password
            )

            # Create New Employee
            Employee.objects.create(
                user = new_user,
                name = name,
                assigned_company = company
            )

            # Create Employee Permission
            EmployeePermission.objects.create(
                user = new_user
            )
            messages.success(request, "new employee created with defalut premissions")
            return redirect('create')



       