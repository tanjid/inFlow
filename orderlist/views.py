from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from _keenthemes.__init__ import KTLayout
from orders.models import NewOrder, DeliveryMethod
from employees.models import Employee
from _keenthemes.libs.theme import KTTheme
from django.contrib.auth.mixins import LoginRequiredMixin
from orders.models import NewOrder, OrderDetails
from django.contrib import messages

# Create your views here.
class Home(ListView):
    template_name = 'orderlist/home.html'
    context_object_name = 'new_order'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        KTTheme.addVendor('m_datatables')
        return context

    def get_queryset(self):
        
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        new_order = NewOrder.objects.filter(company = company_name, is_active=True).distinct()
        latest = NewOrder.objects.filter(company = company_name).distinct()[:5]
        new_order = latest + new_order
        return new_order



class OrderDm(TemplateView):
    template_name = 'orderlist/order_dm.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context['status_name'] = self.kwargs['st']
        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        context['dm_list'] = DeliveryMethod.objects.all()
        context['new_order'] = NewOrder.objects.all()
        return context
        # KTTheme.addJavascriptFile('js/custom/test.js')


class OrderHome(TemplateView):
    template_name = 'orderlist/order_home.html'
    success_message = "was created successfully"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context


class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'orderlist/orders.html'
    login_url = '/employees/login/'
    context_object_name = 'new_order'

    

    def get_context_data(self, **kwargs):
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # context['new_order'] = NewOrder.objects.filter(delivery_method=dm, items__status = status_name).distinct()
        status_name = self.kwargs['st']
        dm = self.kwargs['dm']       
        context['latest'] = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name).distinct().order_by('-created_at')[:5]
        context['status_name'] = status_name
        KTTheme.addJavascriptFile('js/custom/order_list.js')
        if status_name == "Printed":
        #     print(status_name)
            KTTheme.addVendor('m_datatables')



        return context


    def get_queryset(self):
        status_name = self.kwargs['st']
        dm = self.kwargs['dm']
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name, is_active=True).distinct()
        return new_order

        

    def post(self, request, *args, **kwargs):
        company = Employee.objects.get(user = request.user)

        if 'bulk' in request.POST:
            # orders = request.POST.getlist('selected-order')
            # for order in orders:
            #     my_order = NewOrder.objects.get(pk=order)
            #     bulk_update_list = []
            #     for order in my_order.orderdetails_set.all():
            #         order.status = "Shipping"
            #         # order.save()
            #         bulk_update_list.append(order)
            #     OrderDetails.objects.bulk_update(bulk_update_list, ['status'])
            
            
            # messages.add_message(request, messages.SUCCESS, f'{len(orders)} Orders sent to shipping')
            return redirect('index')

        elif 'invoice' in request.POST:
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
            
                # OrderDetails.objects.bulk_update(bulk_update_list, ['status'])
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

            context = {
                'order_list': multi_order_list,
                'company': company,
            }
            return render(request, 'orders/invoice.html', context)
            
        elif 'stock' in request.POST:
            messages.add_message(request, messages.ERROR, f'Something wentwrong')
            return redirect('index')
            order_list = []
            orders = request.POST.getlist('selected-order')
            for order in orders:
                my_order = NewOrder.objects.get(pk=order)
                print(my_order.id)
                order_list.append(my_order)
            
            sku_dict = {}

            for order in order_list:
                # skus = order.items.all()
                skus = order.orderdetails_set.all()
                order_id = order
                for sku in skus:

                    if sku.sku in sku_dict:
                        sku_dict[sku.sku].append(order_id)

                    else:
                        sku_dict[sku.sku] = [order_id]
            
            company = Employee.objects.get(user=request.user).assigned_company
            
            context = {
                'order_list': sku_dict,
                'company': company,
            }
            # print(request.user)
            return render(request, 'orders/stock_checklist.html', context)

class CompleteListView(LoginRequiredMixin, ListView):
    template_name = 'orders/orders.html'
    login_url = '/employees/login/'
    paginate_by = 10
    context_object_name = 'new_order'



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # context['new_order'] = NewOrder.objects.filter(delivery_method=dm, items__status = status_name).distinct()
        status_name = "Complete"
        dm = self.kwargs['dm']       
        
        context['status_name'] = status_name
        KTTheme.addJavascriptFile('js/custom/order_list.js')
        # if status_name == "Printed":
        # #     print(status_name)
        #     KTTheme.addVendor('m_datatables')



        return context


    def get_queryset(self):
        status_name = "Complete"
        dm = self.kwargs['dm']
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name, is_active=True).distinct()
        return new_order

class ReturnListView(LoginRequiredMixin, ListView):
    template_name = 'orders/orders.html'
    login_url = '/employees/login/'
    paginate_by = 10
    context_object_name = 'new_order'



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # context['new_order'] = NewOrder.objects.filter(delivery_method=dm, items__status = status_name).distinct()
        status_name = "Return"
        dm = self.kwargs['dm']       
        
        context['status_name'] = status_name
        KTTheme.addJavascriptFile('js/custom/order_list.js')
        # if status_name == "Printed":
        # #     print(status_name)
        #     KTTheme.addVendor('m_datatables')



        return context


    def get_queryset(self):
        status_name = "Return"
        dm = self.kwargs['dm']
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name, is_active=True).distinct()
        return new_order
        
class CancelListView(LoginRequiredMixin, ListView):
    template_name = 'orders/orders.html'
    login_url = '/employees/login/'
    paginate_by = 10
    context_object_name = 'new_order'



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # context['new_order'] = NewOrder.objects.filter(delivery_method=dm, items__status = status_name).distinct()
        status_name = "Cancel"
        dm = self.kwargs['dm']       
        
        context['status_name'] = status_name
        KTTheme.addJavascriptFile('js/custom/order_list.js')
        # if status_name == "Printed":
        # #     print(status_name)
        #     KTTheme.addVendor('m_datatables')



        return context

    def get_queryset(self):
        status_name = "Cancel"
        dm = self.kwargs['dm']
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name, is_active=True).distinct()
        return new_order
