from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # ...

    path('home/', MktHome.as_view(), name='mkt_home'),
    path('new_order/', MktNewOrderView.as_view(), name='mkt_new_order'),
    path('search/<str:obj>', MktSearch.as_view(), name='mkt_search'),
    path('morders/', MktOrdersView.as_view(), name='mkt_orders'),
    path('morders/<str:shop>', MktNewOrderView.as_view(), name='mkt_orders_n'),
    path('confirm/<str:obj>/<int:order_id>', confirm_order, name='mkt_confirm'),

    # ...
]