from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # ...

    path('', MypageView.as_view(), name='purchase'),
    path('new_purchase', NewPurchaseView.as_view(), name='new_purchase'),
    path('purchase_list', PurchaseListView.as_view(), name='purchase_list'),

    # ...
]