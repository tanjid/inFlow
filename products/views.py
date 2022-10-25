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
from .forms import AdjustStockForm
from django.db.models import Count, F, Value
# Create your views here.
class CurrentStockListView(ListView):
    model = Product
    template_name = 'products/current_stock_list.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        KTTheme.addJavascriptFile('js/custom/current_stock.js')
        KTTheme.addVendor('m_datatables')
        

        return context

class AdjustStockListView(ListView):
    model = AdjustStock
    template_name = 'products/adjust_stock_list.html'
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        KTTheme.addJavascriptFile('js/custom/current_stock.js')
        KTTheme.addVendor('m_datatables')
        

        return context


class AdjustStockView(FormMixin, TemplateView):
    template_name = 'products/adjust_stock.html'
    form_class = AdjustStockForm
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)



        KTTheme.addJavascriptFile('js/custom/adjust_stock.js')
        

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        current_employee = Employee.objects.get(user=request.user)
        if form.is_valid():
            AdjustStock.objects.create(
                sku = Product.objects.get(sku=form.cleaned_data['sku']),
                qty = form.cleaned_data['qty'],
                cause = form.cleaned_data['cause'],
                note = form.cleaned_data['note'],
                by = current_employee,
            )
            Product.objects.get(sku=form.cleaned_data['sku']).decrese_stock(form.cleaned_data['qty'])


            messages.add_message(request, messages.SUCCESS, 'Qty Adjusted Successfully')
            return redirect('adjust_stock')

class LowStockView(TemplateView):
    template_name = 'products/low_stock_notification.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        context['object_list'] = LowStock.objects.filter(active=True)
        context['object_list_stock'] = StockIn.objects.filter(active=True)
        return context


def click_website(request, low_stock_id):
    low_object = LowStock.objects.get(pk=low_stock_id)
    low_object.website = True
    low_object.save()

    if low_object.website and low_object.mkt:
        low_object.active = False
        low_object.save()

    return redirect('low_stock')

def click_mkt(request, low_stock_id):
    low_object = LowStock.objects.get(pk=low_stock_id)
    low_object.mkt = True
    low_object.save()

    if low_object.website and low_object.mkt:
        low_object.active = False
        low_object.save()

    return redirect('low_stock')


def stock_click_website(request, stock_id):
    stock_object = StockIn.objects.get(pk=stock_id)
    stock_object.website = True
    stock_object.save()

    if stock_object.website and stock_object.mkt:
        stock_object.active = False
        stock_object.save()

    return redirect('low_stock')



def stock_click_mkt(request, stock_id):
    
    low_object = StockIn.objects.get(pk=stock_id)
    low_object.mkt = True
    low_object.save()

    if low_object.website and low_object.mkt:
        low_object.active = False
        low_object.save()

    return redirect('low_stock')
