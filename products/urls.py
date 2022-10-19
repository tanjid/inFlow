from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # ...

    path('current_stock_list/', CurrentStockListView.as_view(), name='current_stock_list'),
    path('adjust_stock/', AdjustStockView.as_view(), name='adjust_stock'),
    path('adjust_list/', AdjustStockListView.as_view(), name='adjust_list'),

    # ...
]