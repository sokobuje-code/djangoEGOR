
from django.test import TestCase
from django.core.exceptions import ValidationError

from .models import Product


class ProductValidationTest(TestCase):
    def test_negative_price_raises(self):
        p = Product(name='Test', price='-5.00')
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_short_name_raises(self):
        p = Product(name='ab', price='10.00')
        with self.assertRaises(ValidationError):
            p.full_clean()

    def test_valid_product_passes(self):
        p = Product(name='Valid name', price='12.50')
        # should not raise
        p.full_clean()
