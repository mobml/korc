from datetime import datetime
import json
import time

from django.http import HttpResponse
from .models import Product, Ticket
from .serializers import ProductSerializer, TicketItemSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Create your views here.
def index(request):
    return HttpResponse("Vendify - POS system.")


@api_view(['GET'])
def hello_world(request):
    return Response({"message": "Hello, world!"})

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def make_sale(request):

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