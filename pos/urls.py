from django.urls import path, include
from . import views


urlpatterns = [
    path('api/v1/products/', views.product_list_api, name='product_list_api'),
    path('api/v1/make_sale/', views.sale_create_api, name='sale_create_api'),
    path('api/v1/cancel_sale/<int:ticket_id>/', views.sale_cancel_api, name='sale_cancel_api'),
    path('api/v1/ticket/<int:ticket_id>/', views.ticket_get_details_api, name='ticket_get_details_api')
]