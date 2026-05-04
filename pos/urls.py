from django.urls import path, include
from . import views


urlpatterns = [
    path('api/v1/products/', views.product_list, name='product_list'),
    path('api/v1/make_sale/', views.make_sale, name='make_sale'),
    path('api/v1/cancel_sale/', views.cancel_sale, name='cancel_sale'),
    path('api/v1/get_ticket/', views.get_ticket, name='get_ticket')
]