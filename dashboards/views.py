from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import QuickSearchForm
from orders.models import NewOrder
from django.contrib import messages
from django.shortcuts import render, redirect
from datetime import datetime, timedelta
from employees.models import Employee, EmplpyeePoints
from django.db.models import Avg, Count, Min, Sum
import csv
from orders.models import OrderDetails
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""

class DashboardsView(LoginRequiredMixin, TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'dashboards/tesr_file.html'
    login_url = '/employees/login/'

    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        today = datetime.strftime(datetime.now(), '%a')
        today1 = datetime.strftime(datetime.now() - timedelta(1) , '%a')
        today2 = datetime.strftime(datetime.now() - timedelta(2) , '%a')
        today3 = datetime.strftime(datetime.now() - timedelta(3) , '%a')
        today4 = datetime.strftime(datetime.now() - timedelta(4) , '%a')
        today5 = datetime.strftime(datetime.now() - timedelta(5) , '%a')
        today6 = datetime.strftime(datetime.now() - timedelta(6) , '%a')

        context['data1'] = [today6, today5, today4, today3, today2, today1, today]
        
        # Order in Review
        now = datetime.now()
        current_hour = int(now.strftime('%H'))
        current_day = int(now.strftime('%d'))
        context['order_in_review'] = NewOrder.objects.filter(in_review= True)
        total_point_list = []
        em_list = Employee.objects.all()
        label_list = []
        em_points = EmplpyeePoints.objects.filter(created__day=current_day)
        for em in em_list:
            label_list.append(em.name)
            # pass
            # points = EmplpyeePoints.objects.filter(employee = Employee.objects.get(pk=em.id), created__hour=int(current_hour), created= datetime.today())
            # points = points.aggregate(total = Sum('total'))
            hour_list = []
            points_list = []
            
            # context["points"] = points
            for i in range(9,-1, -1):
                hour = current_hour-i
                hour_list.append(hour)
                points = em_points.filter(employee = Employee.objects.get(pk=em.id), created__hour=int(hour))
                points = points.aggregate(total = Sum('total'))

                if points['total']:

                    points_list.append(points['total'])
                else:

                    points_list.append(0)
                # points_list.append(points['total'])

            total_point_list.append(points_list)
        context['hour_list'] = hour_list
        context['points_list'] = points_list
        context['total_point_list'] = total_point_list

        context['label_list'] = label_list
        today = datetime.now().date()
        todays_orders = NewOrder.objects.filter(created_at__date=today)

        sku_count = {}
        em_count = {}
        total_order_count = 0
        total_sku_count = 0
        for order in todays_orders:
            total_order_count += 1
            if order.employee in em_count:
                em_count[order.employee] = em_count.get(order.employee) + 1
            else:
                em_count[order.employee] = 1
            for i in order.orderdetails_set.all():
                total_sku_count += i.qty
                if i.sku in sku_count:
                    sku_count[i.sku] = sku_count.get(i.sku) + i.qty
                else:
                    sku_count[i.sku] = i.qty

        sku_count = sorted(sku_count.items(), key=lambda x: x[1], reverse=True) 
        sku_count = dict(sku_count)
        limit = 10
        first_n = dict(zip(list(sku_count.keys())[:limit], list(sku_count.values())[:limit]))
        context['todays_orders'] = first_n
        em_count = sorted(em_count.items(), key=lambda x: x[1], reverse=True)
        em_count = dict(em_count) 
        em_count = dict(zip(list(em_count.keys())[:limit], list(em_count.values())[:limit]))
        context['em_count'] = em_count
        context['total_order_count'] = total_order_count
        context['total_sku_count'] = total_sku_count

        return context

def approve_order(request, order_id):
    order = NewOrder.objects.get(pk=order_id)
    order.in_review = False
    order.save()
    messages.add_message(request, messages.SUCCESS, f'Order {order.invoice_number} is now approved')

    return redirect('index')

class TestFileView(LoginRequiredMixin, TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'dashboards/tesr_file.html'
    login_url = '/employees/login/'

    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        """
        # Example to get page name. Refer to dashboards/urls.py file.
        url_name = resolve(self.request.path_info).url_name

        if url_name == 'dashboard-2':
            # Example to override settings at the runtime
            settings.KT_THEME_DIRECTION = 'rtl'
        else:
            settings.KT_THEME_DIRECTION = 'ltr'
        """

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # Include vendors and javascript files for dashboard widgets


        return context

class QuickSearchView(TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'dashboards/quick_search.html'
    login_url = '/employees/login/'
    # Predefined function
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        context['form'] = QuickSearchForm()
        try:
            context['objective'] = self.kwargs['res']
        except KeyError:
            context['objective'] = None



        # Include vendors and javascript files for dashboard widgets
        # KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])
        KTTheme.addJavascriptFile('js/custom/quick_search.js')
        KTTheme.addJavascriptFile('js/custom/order_list.js')
        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        form = QuickSearchForm(request.POST)
        current_employee = Employee.objects.get(user=request.user)
        if 'ad_note' in request.POST:

            note = request.POST.get('new_note')
            order_id = request.POST.get('order_id')
            main_order = NewOrder.objects.get(pk=order_id)
            main_order.note = note
            main_order.save()

            # Add Ponts to Employees
            current_employee.add_points("ad_note")



            messages.add_message(request, messages.SUCCESS, f'Note added to {main_order.invoice_number}')
            context['orders'] = [main_order]
            search_contetn_m = request.POST.get('search_contetn_m')
            search_contetn_o = request.POST.get('search_contetn_o')
            if search_contetn_m:
                context['orders'] = NewOrder.objects.filter(mobille_number__icontains = search_contetn_m)
                print(f"search_contetn_m: {search_contetn_m}")
            elif search_contetn_o:
                print(f"search_contetn_o: {search_contetn_o}")
                context['orders'] = NewOrder.objects.filter(invoice_number = search_contetn_o)


            # context['orders'] = request.POST.get('orders')
            
            return self.render_to_response(context)

        if 'return_note' in request.POST:

            note = request.POST.get('new_return_note')
            order_id = request.POST.get('order_id')
            main_order = NewOrder.objects.get(pk=order_id)
            main_order.return_note = note
            main_order.save()

            # Add Ponts to Employee
            current_employee.add_points("rtn_note")


            messages.add_message(request, messages.SUCCESS, f'Rtn Note added to {main_order.invoice_number}')
            context['orders'] = [main_order]
            search_contetn_m = request.POST.get('search_contetn_m')
            search_contetn_o = request.POST.get('search_contetn_o')
            if search_contetn_m:
                context['orders'] = NewOrder.objects.filter(mobille_number__icontains = search_contetn_m)
                # print(f"search_contetn_m: {search_contetn_m}")
            elif search_contetn_o:
                # print(f"search_contetn_o: {search_contetn_o}")
                context['orders'] = NewOrder.objects.filter(invoice_number = search_contetn_o)


            # context['orders'] = request.POST.get('orders')
            
            return self.render_to_response(context)

        if 'invoice' in request.POST:
            multi_order_list = []
            order_list = []
            orders = request.POST.getlist('selected-order')


        # Sorting Order for prnting sku wise
            for order in orders:
                my_order = NewOrder.objects.get(pk=order)
                bulk_update_list = []
                count = 0
                for order in my_order.orderdetails_set.all():
                    order.status = "Printed"
                    bulk_update_list.append(order)

                    if count == 0:
                        print(f"0")
                        order_list.append(my_order)
                    elif count == 1:
                        print(f"1")
                        multi_order_list.append(my_order)
                        order_list.remove(my_order)
                    count += 1
            
                OrderDetails.objects.bulk_update(bulk_update_list, ['status'])
            list_dict = {}
            for item in order_list:
                for it in item.orderdetails_set.all():
                    if list_dict.get(it.sku.sku):
                        list_dict[it.sku.sku].append(item)
                    else:
                        list_dict[it.sku.sku] = [item]
            
            updated_list = list(list_dict.values())
            sorted_list = []

            for l in updated_list:
                sorted_list.extend(l)


            multi_order_list.extend(sorted_list)
            company = Employee.objects.get(user = request.user)
            context = {
                'order_list': multi_order_list,
                'company': company,
            }
            return render(request, 'orders/invoice.html', context)
                        
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            invoive_number = form.cleaned_data['invoive_number']

            if mobile_number:
                orders = NewOrder.objects.filter(mobille_number__icontains = mobile_number)
                search_contetn = mobile_number
                context['search_contetn_m'] = mobile_number

            elif invoive_number:
                orders = NewOrder.objects.filter(invoice_number = invoive_number)
                search_contetn = invoive_number
                context['search_contetn_o'] = invoive_number
            if orders:
                context['orders'] = orders
            else:
                context['no_orders'] = search_contetn

            # Add Ponts to Employee
            current_employee.add_points("search")

        return self.render_to_response(context)