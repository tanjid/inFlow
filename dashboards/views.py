from django.views.generic import TemplateView
from django.views.generic.edit import FormMixin
from django.http import HttpResponse
from django.conf import settings
from django.urls import resolve
from _keenthemes.__init__ import KTLayout
from _keenthemes.libs.theme import KTTheme
from pprint import pprint
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import QuickSearchForm
from orders.models import NewOrder
from django.shortcuts import render, redirect
"""
This file is a view controller for multiple pages as a module.
Here you can override the page view layout.
Refer to dashboards/urls.py file for more pages.
"""

class DashboardsView(LoginRequiredMixin, TemplateView):
    # Default template file
    # Refer to dashboards/urls.py file for more pages and template files
    template_name = 'pages/dashboards/index.html'
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
        KTTheme.addVendors(['amcharts', 'amcharts-maps', 'amcharts-stock'])

        return context

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
        if form.is_valid():
            mobile_number = form.cleaned_data['mobile_number']
            invoive_number = form.cleaned_data['invoive_number']

            if mobile_number:
                orders = NewOrder.objects.filter(mobille_number__icontains = mobile_number)
                search_contetn = mobile_number
            elif invoive_number:
                orders = NewOrder.objects.filter(invoice_number = invoive_number)
                search_contetn = orders
            if orders:
                context['orders'] = orders
            else:
                context['no_orders'] = search_contetn

        return self.render_to_response(context)