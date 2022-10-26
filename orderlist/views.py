from django.shortcuts import render
from django.views.generic import TemplateView
from _keenthemes.__init__ import KTLayout
# Create your views here.
class Home(TemplateView):
    template_name = 'orderlist/home.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context = KTLayout.init(context)
        return context