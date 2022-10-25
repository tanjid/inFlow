
from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from django.views.generic.edit import FormMixin
from .forms import NewPurchaseForm
from .models import Purchase, PurchaseItems
from products.models import Product
from django.contrib import messages

from django.views.generic.list import ListView
# Create your views here.

class MypageView(TemplateView):
    template_name = 'purchase/purchase_home.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/test.js')
        


        KTTheme.addJavascriptFile('purchase/scripts.js')
        return context

class PurchaseListView(ListView):
    template_name = 'purchase/purchase_list.html'
    paginate_by = 2
    model = Purchase
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/test.js')
        


        KTTheme.addJavascriptFile('purchase/scripts.js')
        return context

class NewPurchaseView(FormMixin, TemplateView):
    form_class = NewPurchaseForm

    template_name = 'purchase/new_purchase.html'

    def get_context_data(self, **kwargs):
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)

        # A function to init the global layout. It is defined in _keenthemes/__init__.py file
        context = KTLayout.init(context)

        # KTTheme.addJavascriptFile('js/custom/test.js')
        


        KTTheme.addJavascriptFile('purchase/scripts.js')
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        grand_total = request.POST.get("grand_total")
        if form.is_valid():
            skus = request.POST.getlist('sku_list')
            qtys = request.POST.getlist('sku_qty')

            new_purchase = Purchase.objects.create(
                purchase_note = form.cleaned_data['purchase_note'],
                grand_total = grand_total,
            )

            for mysku, myqty in zip(skus, qtys):
                selected_sku = Product.objects.get(sku=mysku)
                new_purchsae_item = PurchaseItems.objects.create(
                    sku = selected_sku,
                    qty = myqty,
                )

                new_purchase.items.add(new_purchsae_item)
                # Adding qty to stock
                # selected_sku.stock_qty = int(selected_sku.stock_qty + int(myqty))
                selected_sku.increse_stock(int(myqty))


            messages.add_message(request, messages.SUCCESS, 'Purchase Successful')
            return redirect ("new_purchase")

        else:
            messages.add_message(request, messages.ERROR, 'There was an error try again')
            return redirect ("new_purchase")