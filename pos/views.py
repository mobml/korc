from datetime import datetime
import json

from django.db import transaction
from .models import Product, Ticket, TicketItem
from .serializers import ProductSerializer, TicketItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def make_sale(request):
    with transaction.atomic():

        #first we create a ticket
        ticket = Ticket.objects.create()

        #then we add items to the ticket
        total = 0
        for item in json.loads(request.body):
            ticket_item = TicketItemSerializer(data=item)
            ticket_item.is_valid(raise_exception=True)
            ticket_item.create(ticket_item.validated_data, ticket=ticket)
            total += ticket_item.validated_data['quantity'] * ticket_item.validated_data['price_at_time']

        ticket.total_amount = total
        ticket.status = 'CLOSED'
        ticket.closed_at = datetime.isoformat(datetime.now())
        ticket.save()

        return Response({
            'message': 'Sale processed successfully',
            'details': json.loads(request.body),
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