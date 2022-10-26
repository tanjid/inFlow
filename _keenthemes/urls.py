"""_keenthemes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from _keenthemes.views import SystemView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('orders/', include('orders.urls')),
    path('purchase/', include('purchase.urls')),
    path('employees/', include('employees.urls')),
    path('mkt/', include('market_place_prder.urls')),
    path('reseller/', include('reseller.urls')),
    path('inventory/', include('products.urls')),
    path('order_list/', include('orderlist.urls')),

    # Dashboard urls
    path('search/', include('dashboards.urls')),
    path('', include('dashboards.urls')),

    # Auth urls
    path('', include('auth.urls')),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = SystemView.as_view(template_name = 'pages/system/not-found.html', status=404)
handler500 = SystemView.as_view(template_name = 'pages/system/error.html', status=500)
