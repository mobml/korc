from pos.models import Product, Sale, SaleItem
from pos.serializers import SaleItemSerializer
from django.utils import timezone
from django.db import transaction

"""
Ticket service functions.
"""


def sale_create() -> Sale:
    return Sale.objects.create()


def sale_get(ticket_id: int) -> Sale | None:
    try:
        return Sale.objects.get(id=ticket_id)
    except Sale.DoesNotExist:
        return None


@transaction.atomic()
def sale_and_sale_items_create(sale_items: list) -> Sale:
    sale = sale_create()

    total = 0
    for item in sale_items:
        item = SaleItemSerializer(data=item)
        item.is_valid(raise_exception=True)
        item.create(item.validated_data, sale=sale)
        total += item.validated_data["quantity"] * item.validated_data["price_at_time"]

    sale.total_amount = total
    sale.status = "CLOSED"
    sale.closed_at = timezone.now()
    sale.save()

    return sale


@transaction.atomic()
def sale_cancel(sale: Sale) -> Sale:

    # Firt we find the ticket items for the given ticket
    sale_items = SaleItem.objects.filter(sale_id=sale)

    # Then we update the stock quantities for each item in the ticket
    for item in sale_items:
        product = item.product
        product.stock_quantity += item.quantity
        product.save()

    # Finally we update the ticket status to cancelled
    sale.status = "CANCELLED"
    sale.save()

    return sale


""" TicketItem service functions. """


# Return a list of ticket items for a given ticket, including the product name, quantity, and price at the time of sale.
def sale_items_get_by_sale(sale: Sale) -> list[SaleItem]:

    sale_items = SaleItem.objects.filter(sale_id=sale)
    named_sale_items = []

    for item in sale_items:
        name = Product.objects.get(id=item.product.id).name
        named_sale_items.append(
            {
                "product_name": name,
                "quantity": item.quantity,
                "price_at_time": item.price_at_time,
            }
        )
    return named_sale_items
