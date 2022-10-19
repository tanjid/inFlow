from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # ...

    path('', ResellerHomeView.as_view(), name='res_home'),
    path('res_new_order/', ResellerOrderView.as_view(), name='res_new_order'),
    path('res_orders/', ResellerOrderListView.as_view(), name='res_orders'),

    # ...
]