from django.contrib import admin

# Register your models here.
from .models import Product, Ticket, TicketItem

admin.site.register(Product)
admin.site.register(Ticket)
admin.site.register(TicketItem)