from .models import EmployeePermission, Employee

def get_user_perm(request):

    try:
        current_user = EmployeePermission.objects.get(user=request.user)

    except:

        current_user = None
    try:
        current_employee = Employee.objects.get(user=request.user)

    except:
        current_employee = None


    return {
        'current_user': current_user,
        'current_employee': current_employee,
    }

