from pos.selectors import product_all
from pos.services import sale_cancel, sale_create, ticket_get,  ticket_items_get_by_ticket
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
def cancel_sale(request, ticket_id):
    # First we find the ticket
    
    ticket = ticket_get(ticket_id)
    
    if not ticket:
        return Response(
            {'error': 'Ticket not found'}, 
            status=404
        )
    
    # Then we check if the ticket is already cancelled
    if ticket.status == 'CANCELLED':
        return Response(
            {'error': 'Ticket is already cancelled'}, 
            status=400
        )
    
    if not sale_cancel(ticket):
        return Response(
            {'error': 'Failed to cancel the sale'}, 
            status=500
        )

    return Response({'message': 'Sale cancelled successfully'})

@api_view(['GET'])
def get_ticket(request, ticket_id):
    # First we find the ticket
    
    ticket = ticket_get(ticket_id)

    if not ticket:
        return Response(
            {'error': 'Ticket not found'}, 
            status=404
        )
    
    items = ticket_items_get_by_ticket(ticket)

    return Response({
        'ticket_id': ticket.id,
        'status': ticket.status,
        'total_amount': ticket.total_amount,
        'closed_at': ticket.closed_at,
        'items': items
    })