from .models import LowStock, StockIn
from django.db.models import Q

def get_nitification_count(request):
    low_stock = LowStock.objects.filter(active = True).count()
    stock_in = StockIn.objects.filter(active = True).count()
    return {
        'low_stock': low_stock,
        'stock_in': stock_in,
    }