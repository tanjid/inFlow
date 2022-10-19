from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView, FormView
from django.views.generic.list import ListView
from _keenthemes.__init__ import KTLayout
from .models import *
from _keenthemes.libs.theme import KTTheme
from django.urls import reverse
from django.views.generic.edit import FormMixin
from employees.models import Employee
from django.contrib import messages

# Create your views here.


class ResellerHomeView(TemplateView):
    template_name = 'reseller/res_home.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context

class ResellerOrderView(TemplateView):
    template_name = 'reseller/res_new_order.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)


        context['resellers'] = Reseller.objects.all()


        KTTheme.addJavascriptFile('js/custom/reseller.js')
        

        return context
    def post(self, request, *args, **kwargs):
        reseller_name = request.POST.get("reseller_name")
        reseller = Reseller.objects.get(name=reseller_name)
        sub_total = request.POST.get("item-sub_total")
        grand_total = request.POST.get("grand_total")
        

        skus = request.POST.getlist('sku_list')
        qtys = request.POST.getlist('sku_qty')
        product_prices = request.POST.getlist('product-price')
        item_totals = request.POST.getlist('item-total')

        for i in range(len(skus)):
            selected_sku = Product.objects.get(sku=skus[i])

            if int(selected_sku.stock_qty) < int(qtys[i]):
                messages.add_message(request, messages.ERROR, f'{selected_sku} is out of stock ')
                return redirect('res_new_order')
        
        new_order = ResellerOrder.objects.create(
            reseller_name = reseller,
            sub_total = sub_total,
            grand_total = grand_total,

        )


        for i in range(len(skus)):
            selected_sku = Product.objects.get(sku=skus[i])
            ResellerOrderDetails.objects.create(
                main_order = new_order,
                status = "Complete",
                sku = selected_sku,
                qty = qtys[i],
                product_prices = product_prices[i],
                item_totals = item_totals[i],
            )

            # new_order.items.add(new_order_details)

            # Deducting qty to stock
            # selected_sku.stock_qty = int(selected_sku.stock_qty - int(qtys[i]))
            # selected_sku.save()

        messages.add_message(request, messages.SUCCESS, 'Reseller Order Created Successfully')
        # context = KTLayout.init(context)
        # return render(request, 'market_place_prder/mkt_new_order.html', context)
        return redirect('res_new_order')


class ResellerOrderListView(ListView):
    model = ResellerOrder
    template_name = 'reseller/res_orders.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        # KTTheme.addJavascriptFile('js/custom/test.js')
        

        return context