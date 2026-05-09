from django.test import TestCase
from ..models import Product

class ProductModelTest(TestCase):
    def test_cost_product_cannot_be_greater_than_price(self):
        product = Product(name='Test Product', cost_price=10.00, sale_price=5.00)
        
        with self.assertRaises(ValueError):
            product.full_clean()