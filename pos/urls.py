from django.urls import path
from . import views

BASE_URL = 'api/v1/'

urlpatterns = [
    path(f'{BASE_URL}products/', views.product_list_api, name='product_list_api'),
    path(f'{BASE_URL}sales/', views.sale_create_api, name='sale_create_api'),
    path(f'{BASE_URL}sales/<int:sale_id>/cancel/', views.sale_cancel_api, name='sale_cancel_api'),
    path(f'{BASE_URL}sales/<int:sale_id>/ticket/', views.ticket_get_details_api, name='ticket_get_details_api')
]
