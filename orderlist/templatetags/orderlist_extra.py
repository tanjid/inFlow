from trace import Trace
from django import template
from orders.models import NewOrder, OrderDetails
from employees.models import Employee
from django.utils.safestring import mark_safe
from django.core.paginator import Paginator
register = template.Library()
from django.db.models import Q

@register.simple_tag
def get_proper_elided_page_range(p, number, on_each_side=1, on_ends=1):
    paginator = Paginator(p.object_list, p.per_page)
    return paginator.get_elided_page_range(number=number, 
                                           on_each_side=on_each_side,
                                           on_ends=on_ends)



@register.filter(name='calculate_qty')
def calculate_qty(value):
    quantity = 0
    for item in value:
        for dt in item.orderdetails_set.all():
            quantity += dt.qty

    return quantity

@register.filter(name='calculate_t_qty')
def calculate_t_qty(value):
    quantity = 0
    for dt in value.orderdetails_set.all():
        quantity += dt.qty

    return quantity


@register.filter(name='st_order_count')
def st_order_count(value):
    # order_count = NewOrder.objects.filter(items__status=value).distinct().count()
    order_count = OrderDetails.objects.filter(main_order__is_active=True, status = value).distinct('main_order').count()
    return ""


@register.simple_tag
def order_dm_count( st, dm, user):
    company_name= Employee.objects.get(user=user).assigned_company
    order_count = OrderDetails.objects.filter(main_order__delivery_method=dm, status=st, main_order__company=company_name, main_order__is_active=True).distinct('main_order').count()
    return ""
    
@register.simple_tag
def get_actions(orders):
    # print(f"or_id{orders.id}")
    status_list = []
    for order in orders.orderdetails_set.all():
        status_list.append(order.status)
        # print(f"order-status: {order.status}")
    main = '<div class="menu menu-sub menu-sub-dropdown menu-column menu-rounded menu-gray-600 menu-state-bg-light-primary fw-semibold fs-7 w-125px py-4" data-kt-menu="true" style="">'
    confirm = f'<div class="menu-item px-3"><a href="/orders/confirm_order/{orders.id}" class="menu-link px-3"data-kt-users-table-filter="delete_row">Confirm</a></div>' 
    edit = f'<div class="menu-item px-3" id=""><a href="/orders/edit_order/{orders.id}"class="menu-link px-3" id="edit-button" >Edit</a></div>'
    exchange = f'<div class="menu-item px-3"><a href="/orders/exchange_order/{orders.id}"class="menu-link px-3" id="exchange-button">Exchange</a></div>'
    return_order = f'<div class="menu-item px-3"><a href="/orders/return_order/{orders.id}"class="menu-link px-3" id="exchange-button">Return</a></div>'
    cancel_order = f'<div class="menu-item px-3"><a href="/orders/cancel_order/{orders.id}"class="menu-link px-3" id="exchange-button">Cancel</a></div>'
    confirm_sigle_order = f'<div class="menu-item px-3"><a href="/orders/confirm_sigle_order/{orders.id}"class="menu-link px-3" id="exchange-button">Par Confirm</a></div>'

    if "Shipping" in status_list:
        code = mark_safe(f'{main}{confirm}{return_order}{confirm_sigle_order}</div>')
    elif "Initial" in status_list:
        code = mark_safe(f'{main}{cancel_order}{edit}</div>')
    elif "Printed" in status_list:
        code = mark_safe(f'{main}{cancel_order}{edit}</div>')
    elif "Complete" in status_list:
        code = mark_safe(f'{main}{exchange}</div>')
    else:
        code = mark_safe(f'{main}</div>')
    return code



