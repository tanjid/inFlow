from django.urls import path
from orders.views import TestMessage, OrderListView, NewOrderView, OrderHome, CompleteListView, ReturnListView, CancelListView, OrderDm, EditOrder
from orders.views import confirm_order, SingleConfirmView, ExchangeOrder, ReturnOrder, return_single, confirm_single, cancel_order, ExchangeItems, load_order_data, load_mobile_data

urlpatterns = [
    # ...

    path('test_message/', TestMessage.as_view(), name='test_message'),
    path('new_order/', NewOrderView.as_view(), name='new_order'),
    
    path('load_order_data/', load_order_data, name='load_order_data'),
    path('load_mobile_data/<str:mobile_number>', load_mobile_data, name='load_mobile_data'),
    path('order_home/', OrderHome.as_view(), name='order_home'),

    path('order_list/<str:dm>/Complete', CompleteListView.as_view(), name='complete_list'),
    path('order_list/<str:dm>/Return', ReturnListView.as_view(), name='return_list'),
    path('order_list/<str:dm>/Cancel', CancelListView.as_view(), name='cancel_list'),
    path('order_list/<str:dm>/Cancel', CompleteListView.as_view(), name='cancel_list'),

    path('order_list/<str:dm>/<str:st>', OrderListView.as_view(), name='order_dt_list'),
    path('order_dm/<str:st>', OrderDm.as_view(), name='order_dm'),
    path('edit_order/<int:order_id>', EditOrder.as_view(), name='edit_order'),
    path('confirm_order/<int:order_id>', confirm_order, name='confirm_order'),
    path('confirm_sigle_order/<int:order_id>', SingleConfirmView.as_view(), name='confirm_sigle_order'),
    path('exchange_order/<int:order_id>', ExchangeOrder.as_view(), name='exchange_order'),
    path('return_order/<int:order_id>', ReturnOrder.as_view(), name='return_order'),
    path('return_single/<int:order_id>', return_single, name='return_single'),
    path('confirm_single/<int:order_id>', confirm_single, name='confirm_single'),
    path('cancel_order/<int:order_id>', cancel_order, name='cancel_order'),
    path('exchange_item/<int:order_id>', ExchangeItems.as_view(), name='exchange_item'),

    # ...
]