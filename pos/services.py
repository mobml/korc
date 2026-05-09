from pos.models import Product, Ticket, TicketItem
from pos.serializers import TicketItemSerializer
from django.utils import timezone
from django.db import transaction

"""
Ticket service functions.
"""

def ticket_create() -> Ticket:
    return Ticket.objects.create()

def ticket_get(ticket_id: int) -> Ticket | None:
    try:
        return Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return None

@transaction.atomic()
def sale_create(ticket_items: list) -> Ticket:
    ticket = ticket_create()
    
    total = 0
    for item in ticket_items:
            ticket_item = TicketItemSerializer(data=item)
            ticket_item.is_valid(raise_exception=True)
            ticket_item.create(ticket_item.validated_data, ticket=ticket)
            total += ticket_item.validated_data['quantity'] * ticket_item.validated_data['price_at_time']
    
    ticket.total_amount = total
    ticket.status = 'CLOSED'
    ticket.closed_at = timezone.now()
    ticket.save()

    return ticket

""" TicketItem service functions. """

def ticket_item_get_by_ticket(ticket: Ticket) -> list[TicketItem]:

    ticket_items = TicketItem.objects.filter(ticket_id=ticket)
    named_ticket_items = []

    for item in ticket_items:
        name = Product.objects.get(id=item.product.id).name
        named_ticket_items.append({
            'product_name': name,
            'quantity': item.quantity,
            'price_at_time': item.price_at_time
        })
    return named_ticket_items