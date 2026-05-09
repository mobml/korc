from django.db import transaction

from pos.selectors import product_all
from pos.services import sale_create
from pos.models import Product, Ticket, TicketItem
from pos.serializers import TicketItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def product_list(request):
    return Response(product_all())

@api_view(['POST'])
def make_sale(request):

    ticket = sale_create(request.data)

    return Response({
        'message': 'Sale processed successfully',
        'details': request.data,
        'ticket_id': ticket.id
    })
    
@api_view(['POST'])
def cancel_sale(request):
    ticket_id = request.query_params.get('ticket_id')

    # First we find the ticket
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=404)
    
    # Then we check if the ticket is already cancelled
    if ticket.status == 'CANCELLED':
        return Response({'error': 'Ticket is already cancelled'}, status=400)
    
    # Then we update the stock quantities for each item in the ticket
    ticket_items = TicketItem.objects.filter(ticket_id=ticket)

    with transaction.atomic():

        for item in ticket_items:
            product = item.product_id
            product.stock_quantity += item.quantity
            product.save()
    
        # Finally we update the ticket status to cancelled
        ticket.status = 'CANCELLED'
        ticket.save()
        return Response({'message': 'Sale cancelled successfully'})

@api_view(['GET'])
def get_ticket(request):
    ticket_id = request.query_params.get('ticket_id')

    # First we find the ticket
    try:
        ticket = Ticket.objects.get(id=ticket_id)
    except Ticket.DoesNotExist:
        return Response({'error': 'Ticket not found'}, status=404)
    
    # Then we get the items in the ticket
    ticket_items = TicketItem.objects.filter(ticket_id=ticket)
    items_data = []
    for item in ticket_items:
        name = Product.objects.get(id=item.product_id.id).name
        items_data.append({
            'product_name': name,
            'quantity': item.quantity,
            'price_at_time': item.price_at_time
        })
    
    return Response({
        'ticket_id': ticket.id,
        'status': ticket.status,
        'total_amount': ticket.total_amount,
        'closed_at': ticket.closed_at,
        'items': items_data
    })