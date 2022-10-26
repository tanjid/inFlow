from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # ...

    # path('home/', Home.as_view(), name='oder_list_home'),
    path('oder_list_dm/<str:st>', OrderDm.as_view(), name='oder_list_dm'),
    path('order_home/', OrderHome.as_view(), name='oder_list_home'),
    path('order_list/<str:dm>/<str:st>', OrderListView.as_view(), name='orderlist_dt_list'),
    # ...
]