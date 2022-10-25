from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # ...

    path('current_stock_list/', CurrentStockListView.as_view(), name='current_stock_list'),
    path('adjust_stock/', AdjustStockView.as_view(), name='adjust_stock'),
    path('adjust_list/', AdjustStockListView.as_view(), name='adjust_list'),
    path('low_stock/', LowStockView.as_view(), name='low_stock'),
    path('click_website/<int:low_stock_id>', click_website, name='click_website'),
    path('click_mkt/<int:low_stock_id>', click_mkt, name='click_mkt'),
    path('stock_click_website/<int:stock_id>', stock_click_website, name='stock_click_website'),
    path('stock_click_mkt/<int:stock_id>', stock_click_mkt, name='stock_click_mkt'),

    # ...
]