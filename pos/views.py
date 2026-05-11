from pos.selectors import product_all
from pos.services import (
    sale_cancel,
    sale_create,
    sale_get,
    sale_and_sale_items_create,
    sale_items_get_by_sale,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(["GET"])
def product_list_api(request):
    return Response(product_all())


@api_view(["POST"])
def sale_create_api(request):

    sale = sale_and_sale_items_create(request.data)

    return Response(
        {
            "message": "Sale processed successfully",
            "details": request.data,
            "ticket_id": sale.id,
        }
    )


@api_view(["POST"])
def sale_cancel_api(request, sale_id):
    # First we find the ticket

    sale = sale_get(sale_id)

    if not sale:
        return Response({"error": "Sale not found"}, status=404)

    # Then we check if the ticket is already cancelled
    if sale.status == "CANCELLED":
        return Response({"error": "Sale is already cancelled"}, status=400)

    if not sale_cancel(sale):
        return Response({"error": "Failed to cancel the sale"}, status=500)

    return Response({"message": "Sale cancelled successfully"})


@api_view(["GET"])
def ticket_get_details_api(request, sale_id):
    # First we find the ticket

    sale = sale_get(sale_id)

    if not sale:
        return Response({"error": "Ticket not found"}, status=404)

    items = sale_items_get_by_sale(sale)

    return Response(
        {
            "ticket_id": sale.id,
            "status": sale.status,
            "total_amount": sale.total_amount,
            "closed_at": sale.closed_at,
            "items": items,
        }
    )

