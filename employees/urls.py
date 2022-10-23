from django.urls import path
from .views import *
from . import views


urlpatterns = [
    # ...

    path('', EmplyeesHome.as_view(), name='employess_home'),
    path('logout/', logout_view, name='logout'),
    path('login/', LoginView.as_view(), name='login'),
    path('employee_edit/<pk>', EmployeeEdit.as_view(), name='employee_edit'),
    path('employee_permission_edit/<pk>', EmployeePermissionEdit.as_view(), name='employee_permission_edit'),

    # ...
]