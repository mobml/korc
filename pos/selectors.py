from pos.models import Product
from pos.serializers import ProductSerializer

"""
Product selectors functions.
"""
def product_all():
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return serializer.data