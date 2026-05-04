from django.db import models

class StatusTicket(models.TextChoices):
    OPEN = 'OPEN', 'Open'
    CLOSED = 'CLOSED', 'Closed'
    CANCELLED = 'CANCELLED', 'Cancelled'

# Create your models here.
class Product(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, editable=False)
    name = models.CharField(max_length=255, null=False, editable=True)
    sku = models.CharField(max_length=255, null=True, editable=True)
    stock_quantity = models.IntegerField(null=False, editable=True, default=0)
    cost_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=True)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, editable=False)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=True, default=0.00)
    status = models.CharField(max_length=20, choices=StatusTicket.choices, default=StatusTicket.OPEN, null=False, editable=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False, null=False)
    closed_at = models.DateTimeField(null=True, editable=False)

class TicketItem(models.Model):
    id = models.AutoField(primary_key=True, unique=True, null=False, editable=False)
    product_id = models.ForeignKey(Product, null=False, editable=False, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, editable=False)
    price_at_time = models.DecimalField(max_digits=10, decimal_places=2, null=False, editable=False)
    ticket_id = models.ForeignKey(Ticket, null=False, editable=False, on_delete=models.CASCADE)
    closed_at = models.DateTimeField(null=True, editable=False, auto_now_add=True)