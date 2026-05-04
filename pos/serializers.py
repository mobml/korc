from .models import Product, Ticket, TicketItem
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class TicketItemSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField()
    price_at_time = serializers.DecimalField(max_digits=10, decimal_places=2)

    def create(self, validated_data, ticket):
        product = Product.objects.get(id=validated_data['product_id'])
        ticket_item = TicketItem.objects.create(
            product_id=product,
            quantity=validated_data['quantity'],
            price_at_time=validated_data['price_at_time'],
            ticket_id=ticket
        )
        # Update stock quantity
        product.stock_quantity -= validated_data['quantity']
        product.save()
        return ticket_item

    def validate(self, data):
        # Validate that the product exists
        try:
            product = Product.objects.get(id=data['product_id'])
        except Product.DoesNotExist:
            raise serializers.ValidationError("Product does not exist.")

        # Validate that there is enough stock
        if data['quantity'] > product.stock_quantity:
            raise serializers.ValidationError("Not enough stock available.")
        
        if data['quantity'] <= 0:
            raise serializers.ValidationError("Quantity must be greater than zero.")
        
        if data['price_at_time'] == None:
            raise serializers.ValidationError("Price at time is required.")

        if data['price_at_time'] <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
    
        if data['price_at_time'] < product.cost_price:
            raise serializers.ValidationError("Price cannot be less than cost price.")

        return data
    