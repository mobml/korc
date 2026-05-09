from pos.models import Ticket
from pos.serializers import TicketItemSerializer
from django.utils import timezone
from django.db import transaction

"""
Ticket service functions.
"""

def ticket_create() -> Ticket:
    return Ticket.objects.create()

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