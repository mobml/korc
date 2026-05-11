from decimal import Decimal

from django.db import models
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError


# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)

    sku = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        unique=True,
    )
    stock_quantity = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    cost_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(Decimal("0.00"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(cost_price__gte=0), name="cost_price_non_negative"
            ),
            models.CheckConstraint(
                condition=models.Q(sale_price__gte=0), name="sale_price_non_negative"
            ),
            models.CheckConstraint(
                condition=models.Q(stock_quantity__gte=0),
                name="stock_quantity_non_negative",
            ),
        ]

    def clean(self):
        if self.cost_price > self.sale_price:
            raise ValidationError("Sale price cannot be less than cost price.")

    def __str__(self):
        return self.name


class Sale(models.Model):
    class StatusSale(models.TextChoices):
        OPEN = "OPEN", "Open"
        CLOSED = "CLOSED", "Closed"
        CANCELLED = "CANCELLED", "Cancelled"

    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.00,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    status = models.CharField(
        max_length=20, choices=StatusSale.choices, default=StatusSale.OPEN
    )

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    closed_at = models.DateTimeField(null=True, editable=False)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(total_amount__gte=0),
                name="total_amount_non_negative",
            ),
        ]

    def __str__(self):
        return f"Ticket {self.id} - {self.status}"


class SaleItem(models.Model):
    product = models.ForeignKey(
        Product, editable=False, on_delete=models.CASCADE, related_name="sale_items"
    )

    quantity = models.IntegerField(editable=False, validators=[MinValueValidator(1)])

    price_at_time = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        validators=[MinValueValidator(Decimal("0.00"))],
    )

    sale = models.ForeignKey(
        Sale, editable=False, on_delete=models.CASCADE, related_name="items"
    )

    class Meta:
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0), name="quantity_positive"
            ),
            models.CheckConstraint(
                condition=models.Q(price_at_time__gte=0),
                name="price_at_time_non_negative",
            ),
        ]

    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    closed_at = models.DateTimeField(null=True, blank=True, editable=False)

