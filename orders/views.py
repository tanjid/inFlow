
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView
from _keenthemes.__init__ import KTLayout
from .models import *
from _keenthemes.libs.theme import KTTheme
from django.urls import reverse

from .forms import NewOrderForm
from django.contrib import messages
from django.http import JsonResponse
from products.models import Product
from employees.models import Employee
from django.views.generic.edit import FormMixin
import random
from .models import NewOrder, OrderDetails
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import CreateView
from pytz import timezone
from datetime import datetime

# Create your views here.
UTC = timezone('Asia/Kolkata')

def test_message(request):
    messages.add_message(request, messages.INFO, 'Hellao world.')

    return render(request, 'orders/test_message.html')

class TestMessage(SuccessMessageMixin, CreateView):
    template_name = 'orders/test_message.html'
    model = DeliveryMethod
    fields = "__all__"
    success_message = " was created successfully"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        context['dm_list'] = DeliveryMethod.objects.all()
        context['new_order'] = NewOrder.objects.all()
        return context
        # KTTheme.addJavascriptFile('js/custom/test.js')

    def get_success_url(self):
        return reverse('test_message')



class EditOrder(FormMixin, TemplateView):
    template_name = 'orders/edit_order.html'
    form_class = NewOrderForm
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        order_id = self.kwargs['order_id']
        order = NewOrder.objects.get(id=order_id)

        order_details = order.orderdetails_set.all()
        delivery_method = order.delivery_method

        initial_dict = {
            "name" : order.name,
            "number" : order.mobille_number,
            "address" : order.address,
            "order_note" : order.note,
            "sub_total" : order.sub_total,
            "advance" : order.advance,
            "discount" : order.discount,
            "delivery_charge" : order.delivery_charge,
            "grand_total" : order.total_price,

        }
        context['form'] = NewOrderForm(initial=initial_dict)
        context['order_details'] = order_details
        context['de_m'] = DeliveryMethod.objects.all()
        context['delivery_method'] = delivery_method
        context['order_invoice'] = order.invoice_number
        KTTheme.addJavascriptFile('js/custom/order_edit.js')
        return context
        # KTTheme.addJavascriptFile('js/custom/test.js')

    def post(self, request, *args, **kwargs):
        order_id = self.kwargs['order_id']
        form = self.get_form()
        if form.is_valid():
            del_method = request.POST.get("delivery_method")
            # Deleteing old items
            
            order = NewOrder.objects.get(id=order_id)
            order_details = order.orderdetails_set.all()

            for item in order_details:

                # Increment Stock
                product = Product.objects.get(sku=item.sku)
                product.increse_stock(item.qty)


                item.delete()



            order.mobille_number = form.cleaned_data['number']
            order.name = form.cleaned_data['name']
            order.address = form.cleaned_data['address']
            # dm = form.cleaned_data['delivery_method']
            # order.delivery_method = dm
            order.delivery_method = DeliveryMethod.objects.get(name=del_method)
            order.note = form.cleaned_data['order_note']
            order.total_price = form.cleaned_data['grand_total']
            order.delivery_charge = form.cleaned_data['delivery_charge']
            order.discount = form.cleaned_data['discount']
            order.advance = form.cleaned_data['advance']
            order.sub_total = form.cleaned_data['sub_total']
            order.save()

            skus = request.POST.getlist('sku_list')
            qtys = request.POST.getlist('sku_qty')
            product_prices = request.POST.getlist('product-price')
            item_totals = request.POST.getlist('item-total')
            for i in range(len(skus)):
                selected_sku = Product.objects.get(sku=skus[i])
                new_order_details = OrderDetails.objects.create(
                    main_order = order,
                    status = "Initial",
                    sku = selected_sku,
                    qty = qtys[i],
                    product_prices = product_prices[i],
                    item_totals = item_totals[i],
                )

                # order.items.add(new_order_details)

                # Deducting qty to stock
                # selected_sku.stock_qty = int(selected_sku.stock_qty - int(qtys[i]))
                selected_sku.decrese_stock(int(qtys[i]))
                # selected_sku.save()

            messages.add_message(request, messages.SUCCESS, f'Order Edited to Successfully')
            return redirect("edit_order", order_id=order_id)
        else:
            messages.add_message(request, messages.ERROR, f'There was a problem please try again!')
            return redirect("edit_order", order_id=order_id)

class OrderDm(TemplateView):
    template_name = 'orders/order_dm.html'

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
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name).distinct()
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
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name).distinct()
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
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name).distinct()
        return new_order

class OrderListView(LoginRequiredMixin, ListView):
    template_name = 'orders/orders.html'
    login_url = '/employees/login/'
    context_object_name = 'new_order'



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # context['new_order'] = NewOrder.objects.filter(delivery_method=dm, items__status = status_name).distinct()
        status_name = self.kwargs['st']
        dm = self.kwargs['dm']       
        delivery_method = DeliveryMethod.objects.get(pk=dm)
        context['status_name'] = status_name
        context['delivery_method'] = delivery_method
        # KTTheme.addJavascriptFile('js/custom/order_list.js')
        if status_name == "Printed" or status_name == "Initial":
            KTTheme.addVendor('m_datatables')



        return context


    def get_queryset(self):
        status_name = self.kwargs['st']
        dm = self.kwargs['dm']
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        new_order = NewOrder.objects.filter(delivery_method=dm, orderdetails__status = status_name, company = company_name).distinct()
        return new_order

        

    def post(self, request, *args, **kwargs):
        company = Employee.objects.get(user = request.user)
        dm = self.kwargs['dm']
        dm = DeliveryMethod.objects.get(pk=dm)
        date_time = datetime.now(UTC)
        
        if 'bulk' in request.POST:
            print(request.POST)
            orders = request.POST.getlist('selected-order')
            for order in orders:
                my_order = NewOrder.objects.get(pk=order)
                bulk_update_list = []
                for order in my_order.orderdetails_set.all():
                    order.status = "Shipping"
                    # order.save()
                    bulk_update_list.append(order)
                OrderDetails.objects.bulk_update(bulk_update_list, ['status'])
            
            
            messages.add_message(request, messages.SUCCESS, f'{len(orders)} Orders sent to shipping')
            return redirect('test_message')

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

            context = {
                'order_list': multi_order_list,
                'company': company,
            }
            return render(request, 'orders/invoice.html', context)
            
        elif 'stock' in request.POST:
            order_list = []
            orders = request.POST.getlist('selected-order')
            for order in orders:
                my_order = NewOrder.objects.get(pk=order)
                # print(my_order.id)
                order_list.append(my_order)
            
            sku_dict = {}
            sku_qty = 0
            for order in order_list:
                # skus = order.items.all()
                
                skus = order.orderdetails_set.all()
                order_id = order
                for sku in skus:
                    sku_qty += sku.qty
                    # print(sku_qty)
                    if sku.sku in sku_dict:
                        sku_dict[sku.sku].append(order_id)

                    else:
                        sku_dict[sku.sku] = [order_id]
            
            company = Employee.objects.get(user=request.user).assigned_company
            order_inv_count = len(order_list)
            context = {
                'order_list': sku_dict,
                'company': company,
                'delivery_method': dm,
                'date_time': date_time,
                'sku_qty': sku_qty,
                'order_inv_count': order_inv_count,
            }
            # print(request.user)
            return render(request, 'orders/stock_checklist.html', context)

        
        
class OrderHome(TemplateView):
    template_name = 'orders/order_home.html'
    success_message = "was created successfully"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context

# class OrderListView(TemplateView):
#     template_name = 'orders/orders.html'

#     def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
#         context = super().get_context_data(**kwargs)

#         # A function to init the global layout. It is defined in _keenthemes/__init__.py file
#         context = KTLayout.init(context)
#         status_name = self.kwargs['st']
#         dm = self.kwargs['dm']
#         # status_list = ['Initial', 'Assigned', 'Pending', 'Complete', 'Return']
#         context['new_order'] = NewOrder.objects.filter(delivery_method=dm, items__status = status_name)

        

        return context

class NewOrderView(SuccessMessageMixin, FormMixin, TemplateView):
    form_class = NewOrderForm
    initial = {'key': 'value'}
    template_name = 'orders/new_order.html'
    success_message = " was updated successfully"

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        # context['new_order'] = NewOrder.objects.all()
        context['de_m'] = DeliveryMethod.objects.all()

        KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context

    
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        current_employee = Employee.objects.get(user=request.user)

        
        if form.is_valid():
            skus = request.POST.getlist('sku_list')
            qtys = request.POST.getlist('sku_qty')
            product_prices = request.POST.getlist('product-price')
            item_totals = request.POST.getlist('item-total')
            del_method = request.POST.get("delivery_method")
            for i in range(len(skus)):
                selected_sku = Product.objects.get(sku=skus[i])

                if int(selected_sku.stock_qty) < int(qtys[i]):
                    messages.add_message(request, messages.ERROR, f'{selected_sku} available qty is {selected_sku.stock_qty} ')
                    return redirect('new_order')

            get_invoice_number = Employee.get_invoice_number(current_employee)
            while NewOrder.objects.filter(invoice_number=get_invoice_number).exists():
                get_invoice_number = Employee.get_invoice_number(current_employee)
            value = random.randint(0, 9)

            if value == 1:
                active = True
            else:
                active = False
            # print(f"value: {value}, active: {active}")
            new_order = NewOrder.objects.create(
                mobille_number = form.cleaned_data['number'],
                name = form.cleaned_data['name'],
                address = form.cleaned_data['address'],
                delivery_method = DeliveryMethod.objects.get(name=del_method),
                note = form.cleaned_data['order_note'],
                total_price = form.cleaned_data['grand_total'],
                delivery_charge = form.cleaned_data['delivery_charge'],
                discount = form.cleaned_data['discount'],
                advance = form.cleaned_data['advance'],
                sub_total = form.cleaned_data['sub_total'],
                invoice_number = get_invoice_number,
                employee = current_employee,
                company = current_employee.assigned_company,
                is_active = active
            )
            new_order.decide_review_status()

            if new_order.in_review:
                messages.add_message(request, messages.INFO, 'You order in Review Please Notify admin for approval')


            # for mysku, myqty in zip(skus, qtys, product_prices, item_totals):
            #     selected_sku = Product.objects.get(sku=mysku)
            #     new_order_details = OrderDetails.objects.create(
            #         status = "Initial",
            #         sku = selected_sku,
            #         qty = myqty,
            #         product_prices = product_prices,
            #         item_totals = item_totals,
            #     )
            for i in range(len(skus)):
                selected_sku = Product.objects.get(sku=skus[i])
                OrderDetails.objects.create(
                    main_order = new_order,
                    status = "Initial",
                    sku = selected_sku,
                    qty = qtys[i],
                    product_prices = product_prices[i],
                    item_totals = item_totals[i],
                )

                # new_order.items.add(new_order_details)

                # Deducting qty to stock
                selected_sku.decrese_stock(int(qtys[i]))
                # selected_sku.stock_qty = int(selected_sku.stock_qty - int(qtys[i]))
                # selected_sku.save()

            messages.add_message(request, messages.SUCCESS, 'Order Created Successfully')

            # Add Ponts to Employee
            current_employee.add_points("new_order")
            

            return redirect('new_order')
        else:
            messages.add_message(request, messages.ERROR, 'There was a problem try again')  
            return redirect('new_order')

def load_order_data(request):
    print("load order data")
    data = []

    porducts_data = Product.objects.all()

    for obj in porducts_data:
        item = {
            'name': obj.name,
            'sku': obj.sku,
            'sell_price': obj.sell_price,
            'stock_qty': obj.stock_qty,
        }

        data.append(item)
    return JsonResponse({
        'data': data,
    })

def load_mobile_data(request, mobile_number):
    print("load_mobile_data")
    data = []
    try:
        print(f"mobile_number: {mobile_number}")
        mobile_data_list = NewOrder.objects.filter(mobille_number=mobile_number)
        Initial = 0
        Printed = 0
        Shipping = 0
        Complete = 0
        Return = 0
        Exchange = 0
        for details in mobile_data_list:
            for item in details.orderdetails_set.all():
                if item.status == "Initial":
                    Initial += 1
                if item.status == "Printed":
                    Printed += 1
                if item.status == "Shipping":
                    Shipping += 1
                if item.status == "Complete":
                    Complete += 1
                if item.status == "Return":
                    Return += 1
                if item.status == "Exchange":
                    Exchange += 1

        mobile_data = mobile_data_list[0]
        print(f"mobile_data: {mobile_data}")
    except:
        mobile_data = None

    

    if mobile_data:
        item = {
            'name': mobile_data.name,
            'delivery_method': mobile_data.delivery_method.name,
            'note': mobile_data.note,
            'address': mobile_data.address,
            'Initial': Initial,
            'Printed': Printed,
            'Shipping': Shipping,
            'Complete': Complete,
            'Return': Return,
            'Exchange': Exchange,
        }

        data.append(item)
    else:
        item = {}
    return JsonResponse({
        'data': item,
    })


def confirm_order(request, order_id):
    orders = NewOrder.objects.get(id=order_id)
    for order in orders.orderdetails_set.all():

        if order.status == "Shipping":
            order.status = "Complete"
            order.save()
            messages.add_message(request, messages.SUCCESS, f'{order.sku} of {orders.invoice_number} Confirm Successful')

            # Add Ponts to Employee
            current_employee = Employee.objects.get(user=request.user)
            current_employee.add_points("complete_order")
        else:
            messages.add_message(request, messages.ERROR, f'{order.sku} of {orders.invoice_number} is not in Cant be confirmed because its in {order.status}')

    return redirect('search_for_confirm', res = 'con')


def return_single(request, order_id):
    main_order_details = OrderDetails.objects.get(pk=order_id)
    # Increase Stock qty for cancel order
    slec_product = Product.objects.get(sku=main_order_details.sku)
    slec_product.increse_stock(main_order_details.qty)
    # update order status
    main_order_details.status = "Return"
    main_order_details.save()
    # return redirect('test_message')
    # Add Ponts to Employee
    current_employee = Employee.objects.get(user=request.user)
    current_employee.add_points("return_order")
    
    messages.add_message(request, messages.SUCCESS, f'{main_order_details.sku} Returned Successfully!')
    return redirect('return_order',  order_id=main_order_details.main_order.id)

def confirm_single(request, order_id):
    main_order_details = OrderDetails.objects.get(pk=order_id)
    # update order status
    main_order_details.status = "Complete"
    main_order_details.save()

    # Add Ponts to Employee
    current_employee = Employee.objects.get(user=request.user)
    current_employee.add_points("complete_order")


    messages.add_message(request, messages.SUCCESS, f'{main_order_details.sku} Confirmed Successfully!')
    return redirect('confirm_sigle_order',  order_id=main_order_details.main_order.id)


def cancel_order(request, order_id):
    main_order = NewOrder.objects.get(pk=order_id)

    for item in main_order.orderdetails_set.all():
        # Increase Stock qty for cancel order
        slec_product = Product.objects.get(sku=item.sku)
        slec_product.stock_qty += item.qty
        slec_product.save()
        # update order status
        item.status = "Cancel"
        item.save()


    messages.add_message(request, messages.SUCCESS, 'Order Cancel Successful')
    return redirect('test_message')


class SingleConfirmView(TemplateView):
    template_name = 'orders/confirm_order.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        order = NewOrder.objects.get(id=order_id)
        context['order'] = order

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context
class ReturnOrder(TemplateView):
    template_name = 'orders/return_order.html'
    success_message = "was created successfully"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        order = NewOrder.objects.get(id=order_id)
        context['order'] = order

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context

    def post(self, request, *args, **kwargs):

        if "form1" in request.POST:
            order_details_id = request.POST.get('order_details_id')
            order_id = request.POST.get('order_id')
            main_order_details = OrderDetails.objects.get(pk=order_details_id)
            get_name_qty = f"qty{order_id}"
            input_qty = request.POST.get(get_name_qty)


            if int(input_qty) == int(main_order_details.qty):
                messages.add_message(request, messages.INFO, 'No Qty Changed Detected!')
                return redirect('return_order',  order_id=order_id)

            if int(input_qty) < int(main_order_details.qty):
                diff_qty =  int(main_order_details.qty) - int(input_qty)
                # Increse Product stock for diff qty
                slec_product = Product.objects.get(sku=main_order_details.sku)
                # slec_product.stock_qty += diff_qty
                # slec_product.save()
                slec_product.increse_stock(diff_qty)


                main_order_details.qty = int(input_qty)
                main_order_details.save()
                


                messages.add_message(request, messages.SUCCESS, 'Qty Changed Successfully')
                return redirect('return_order',  order_id=order_id)

            messages.add_message(request, messages.SUCCESS, 'Qty Changed Successfully')
            return redirect('return_order',  order_id=order_id)

        if "form2" in request.POST:
            order_id = request.POST.get('order_id')
            order = NewOrder.objects.get(id=order_id)
            order.return_note = request.POST.get('rtn_note')
            order.save()
            messages.add_message(request, messages.SUCCESS, 'Return note added')
            return redirect('return_order',  order_id=order_id)

        if "form_a" in request.POST:
            order_id = request.POST.get('order_id')
            order = NewOrder.objects.get(id=order_id)
            rtn_note = request.POST.get('rtn_note')
            if rtn_note:
                order.return_note = request.POST.get('rtn_note')
                messages.add_message(request, messages.SUCCESS, 'Return note added')
                order.save()

            order_details = order.orderdetails_set.all()
            for item in order_details:
                print(item)
                if item.status == "Shipping":
                    item.status = "Return"
                    item.save()
                    selec_product = Product.objects.get(sku=item.sku)
                    selec_product.increse_stock(qty=item.qty)
                    messages.add_message(request, messages.SUCCESS, f'{item.sku} Returned')

                    # Add Ponts to Employee
                    current_employee = Employee.objects.get(user=request.user)
                    current_employee.add_points("return_order")
                else:
                    messages.add_message(request, messages.ERROR, f'{item.sku} is not Returned Because its in  {item.status}')
            return redirect('return_order',  order_id=order_id)
            # return redirect('search_for_confirm', res='rtn')

class ExchangeOrder(TemplateView):
    template_name = 'orders/exchange_order.html'
    success_message = "was created successfully"
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        order_id = self.kwargs['order_id']
        order = NewOrder.objects.get(id=order_id)
        context['order'] = order

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context

    def post(self, request, *args, **kwargs):
        order_details_id = request.POST.get('order_details_id')
        order_id = request.POST.get('order_id')
        main_order_details = OrderDetails.objects.get(pk=order_details_id)
        get_name_qty = f"qty{order_id}"
        input_qty = request.POST.get(get_name_qty)
        if int(input_qty) == int(main_order_details.qty):
            messages.add_message(request, messages.INFO, 'No Qty Changed Detected!')
            return redirect('return_order',  order_id=order_id)

        if int(input_qty) < int(main_order_details.qty):
            diff_qty =  int(main_order_details.qty) - int(input_qty)
            # Increse Product stock for diff qty
            # print("Increse Product stock for diff qty")
            # print(f"diff_qty: {diff_qty}")
            slec_product = Product.objects.get(sku=main_order_details.sku)
            # slec_product.stock_qty += diff_qty
            slec_product.increse_stock(diff_qty)
            # print(f"after slec_product.stock_qty: {slec_product.stock_qty}")
            slec_product.save()

            main_order_details.qty = int(input_qty)
            main_order_details.save()
            


            messages.add_message(request, messages.SUCCESS, 'Qty Changed Successfully')
            return redirect('return_order',  order_id=order_id)

        messages.add_message(request, messages.SUCCESS, 'Qty Changed Successfully')
        return redirect('return_order',  order_id=order_id)

def exchange_item(request, order_id):
    current_employee = Employee.objects.get(user=request.user)

    main_order_details = OrderDetails.objects.get(pk=order_id)
    print(main_order_details.sku)
    order = main_order_details.main_order
    initial_dict = {
        "name" : order.name,
        "number" : order.mobille_number,
        "delivery_method" : order.delivery_method,
        "address" : order.address,
        "order_note" : order.note,
        "sub_total" : order.sub_total,
        "advance" : order.advance,
        "discount" : order.discount,
        "delivery_charge" : order.delivery_charge,
        "grand_total" : order.total_price,

    }

    # update order status
    main_order_details.status = "Exchange"
    main_order_details.save()
    return redirect('test_message')

class ExchangeItems(FormMixin, TemplateView):
    template_name = 'orders/edit_order.html'
    form_class = NewOrderForm

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        order_id = self.kwargs['order_id']

        order_details = OrderDetails.objects.get(pk=order_id)

        # update order status
        order_details.status = "Exchange"
        order_details.save()

        order = order_details.main_order
        print(f"order_details {order_details}")
        initial_dict = {
            "name" : order.name,
            "number" : order.mobille_number,
            # "delivery_method" : order.delivery_method.name,
            "address" : order.address,
            "order_note" : f"Exchange Order of {order.invoice_number}",
            "sub_total" : order.sub_total,
            "advance" : order.advance,
            "discount" : order.discount,
            "delivery_charge" : order.delivery_charge,
            "grand_total" : order.total_price,

        }
        context['form'] = NewOrderForm(initial=initial_dict)
        context['order_details'] = [order_details]
        context['de_m'] = DeliveryMethod.objects.all()
        context['delivery_method'] = order.delivery_method
        print(f"order.delivery_method {order.delivery_method}")
        KTTheme.addJavascriptFile('js/custom/order_edit.js')
        return context
        # KTTheme.addJavascriptFile('js/custom/test.js')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        current_employee = Employee.objects.get(user=request.user)
        if form.is_valid():
            del_method = request.POST.get("delivery_method")
            new_order = NewOrder.objects.create(
            mobille_number = form.cleaned_data['number'],
            name = form.cleaned_data['name'],
            address = form.cleaned_data['address'],
            # dm = form.cleaned_data['delivery_method']
            # order.delivery_method = dm
            delivery_method = DeliveryMethod.objects.get(name=del_method),
            note = form.cleaned_data['order_note'],
            total_price = form.cleaned_data['grand_total'],
            delivery_charge = form.cleaned_data['delivery_charge'],
            discount = form.cleaned_data['discount'],
            advance = form.cleaned_data['advance'],
            sub_total = form.cleaned_data['sub_total'],
            invoice_number = Employee.get_invoice_number(current_employee),
            employee = current_employee,
            company = current_employee.assigned_company
            )


            skus = request.POST.getlist('sku_list')
            qtys = request.POST.getlist('sku_qty')
            product_prices = request.POST.getlist('product-price')
            item_totals = request.POST.getlist('item-total')
            for i in range(len(skus)):
                selected_sku = Product.objects.get(sku=skus[i])
                OrderDetails.objects.create(
                    main_order = new_order,
                    status = "Initial",
                    sku = selected_sku,
                    qty = qtys[i],
                    product_prices = product_prices[i],
                    item_totals = item_totals[i],
                )

            messages.add_message(request, messages.SUCCESS, 'Order Exchange Successful!!')
            return redirect('test_message')
        else:
            messages.add_message(request, messages.SUCCESS, 'Order Exchange Failed!!')
            return redirect('test_message')



class ROrderListView(LoginRequiredMixin, ListView):
    template_name = 'orders/orders_list.html'
    login_url = '/employees/login/'
    context_object_name = 'new_order'



    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        context = KTLayout.init(context)

        KTTheme.addJavascriptFile('js/custom/order_list.js')
  
        KTTheme.addVendor('m_datatables')



        return context


    def get_queryset(self):
        company_name = Employee.objects.get(user=self.request.user).assigned_company
        new_order = NewOrder.objects.filter(company = company_name).distinct()
        new_order_count = new_order.count()
        print(f"new_order_count: {new_order_count}")
        new_order = new_order[int(new_order_count*.90):]
        return new_order

        

    def post(self, request, *args, **kwargs):
        company = Employee.objects.get(user = request.user)

        if 'bulk' in request.POST:
            print(request.POST)
            orders = request.POST.getlist('selected-order')
            for order in orders:
                my_order = NewOrder.objects.get(pk=order)
                bulk_update_list = []
                for order in my_order.orderdetails_set.all():
                    order.status = "Shipping"
                    # order.save()
                    bulk_update_list.append(order)
                OrderDetails.objects.bulk_update(bulk_update_list, ['status'])
            
            
            messages.add_message(request, messages.SUCCESS, f'{len(orders)} Orders sent to shipping')
            return redirect('test_message')

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

            context = {
                'order_list': multi_order_list,
                'company': company,
            }
            return render(request, 'orders/invoice.html', context)
            
        elif 'stock' in request.POST:
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

        