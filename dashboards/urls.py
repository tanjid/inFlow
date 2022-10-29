from django.urls import path
from dashboards.views import DashboardsView, QuickSearchView, TestFileView
from django.contrib.auth.decorators import login_required
from .views import approve_order

urlpatterns = [
    path('', DashboardsView.as_view(), name='index'),
    path('quick_search/', QuickSearchView.as_view(), name='quick_search'),
    path('search_for/<str:res>/', QuickSearchView.as_view(), name='search_for_confirm'),
    path('quick', TestFileView.as_view(), name='quick'),
    path('approve_order/<str:order_id>', approve_order, name='approve_order'),

    path('error', DashboardsView.as_view(template_name = 'non-exist-file.html'), name='Error Page'),
]