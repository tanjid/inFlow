
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView
from django.views.generic.list import ListView
from django.conf import settings
from _keenthemes.__init__ import KTLayout
from .models import *
from _keenthemes.libs.theme import KTTheme
from django.urls import reverse
from django.views.generic.edit import FormMixin
from .forms import MktNewOrderForm
from employees.models import Employee
from django.contrib import messages
# Create your views here.

class MktHome(TemplateView):
    template_name = 'market_place_prder/mkt_home.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context

class MktNewOrderView(FormMixin,TemplateView):
    template_name = 'market_place_prder/mkt_new_order.html'
    form_class = MktNewOrderForm
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        try:
            shop_n = self.kwargs['shop']
        except:
            shop_n = None
        if shop_n:
            context['shop_name'] = shop_n
        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)
        context['mkt_shops'] = MktShop.objects.all()



        KTTheme.addJavascriptFile('js/custom/mkt_new_order.js')
        

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        shop = request.POST.get("mkt_shop")
        if form.is_valid():
            invoice = form.cleaned_data['invoice']
            if MktOrder.objects.filter(invoice=invoice).exists():
                messages.add_message(request, messages.ERROR, f'Invoice: {invoice} is already exists')
                return redirect('mkt_orders_n', shop = shop)
            else:
                skus = request.POST.getlist('sku_list')
                qtys = request.POST.getlist('sku_qty')
                product_prices = request.POST.getlist('product-price')
                item_totals = request.POST.getlist('item-total')

                for i in range(len(skus)):
                    selected_sku = Product.objects.get(sku=skus[i])

                    if int(selected_sku.stock_qty) < int(qtys[i]):
                        messages.add_message(request, messages.ERROR, f'{selected_sku} is out of stock ')
                        return redirect('mkt_orders_n', shop = shop)
                
                new_order = MktOrder.objects.create(
                    invoice = form.cleaned_data['invoice'],
                    shop_name = MktShop.objects.get(name=shop),
                    sub_total = request.POST.get("item-sub_total"),
                    employee = Employee.objects.get(user=request.user),

                )


                for i in range(len(skus)):
                    selected_sku = Product.objects.get(sku=skus[i])
                    MktOrderDetails.objects.create(
                        main_order = new_order,
                        status = "Shipping",
                        sku = selected_sku,
                        qty = qtys[i],
                        product_prices = product_prices[i],
                        item_totals = item_totals[i],
                    )

                    # new_order.items.add(new_order_details)

                    # Deducting qty to stock
                    # selected_sku.stock_qty = int(selected_sku.stock_qty - int(qtys[i]))
                    # selected_sku.save()

                messages.add_message(request, messages.SUCCESS, 'Mkt Order Created Successfully')
                # context = KTLayout.init(context)
                # return render(request, 'market_place_prder/mkt_new_order.html', context)
                return redirect('mkt_orders_n', shop = shop)
        else:
            messages.add_message(request, messages.ERROR, 'There was a problem try again')  
            return redirect('new_order')
class MktSearch(TemplateView):
    template_name = 'market_place_prder/mkt_search.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        try:
            obj = self.kwargs['obj']
            context['obje'] = obj
        except:
            obj = None

        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context

    def post(self, request, *args, **kwargs):
        invoice = request.POST.get("mkt-invoice")
        context = self.get_context_data(**kwargs)
        order = MktOrder.objects.filter(invoice=invoice)
        action = True
        if order:
            for item in order[0].mktorderdetails_set.all():
                if item.status != "Shipping":
                    action = False
                    messages.add_message(request, messages.ERROR, f'{invoice} is not in shiping. its in {item.status}')  
            if action:
                context['object_list'] = order
        else:
            messages.add_message(request, messages.ERROR, f'No order found with invoice {invoice}')  
        return self.render_to_response(context)


class MktOrdersView(ListView):
    model = MktOrder
    template_name = 'market_place_prder/mkt_orders.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context


def confirm_order(request, obj, order_id):
    orders = MktOrder.objects.get(id=order_id)
    if obj == 'con':
        for order in orders.mktorderdetails_set.all():
            order.status = "Complete"
            order.save()
        messages.add_message(request, messages.SUCCESS, f'{orders.invoice} completed')
        return redirect('mkt_search', obj = 'con')
    elif obj == 'rtn':
        for order in orders.mktorderdetails_set.all():
            order.status = "Return"
            order.save()

            # Increase Stock qty for rtb order
            slec_product = Product.objects.get(sku=order.sku)
            slec_product.stock_qty += order.qty
            slec_product.save()
        messages.add_message(request, messages.SUCCESS, f'{orders.invoice} Returned') 
        return redirect('mkt_search', obj='rtn')
