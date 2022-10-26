from django.urls import path
from .views import *
from . import views

urlpatterns = [
    # ...

    path('home/', Home.as_view(), name='oder_list_home'),


    # ...
]