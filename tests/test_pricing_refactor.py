from decimal import Decimal

import pytest

from sretrans.cart import Cart
from sretrans.invoice import Invoice
from sretrans.pricing import calculate_total, normalize_quantity


def test_cart_and_invoice_agree_on_total():
    cart = Cart([
        {"sku": "A", "price": "10.00", "quantity": 2},
        {"sku": "B", "price": "4.50", "quantity": 1},
    ])

    invoice_lines = [
        {"sku": "A", "price": "10.00", "quantity": 2},
        {"sku": "B", "price": "4.50", "quantity": 1},
    ]

    cart_total = cart.totals(tax_rate=0.10, discount_rate=0.05)
    invoice_total = Invoice.total_for(invoice_lines, tax_rate=0.10, discount_rate=0.05)

    assert cart_total == invoice_total
    assert cart_total["subtotal"] == Decimal("24.50")
    assert cart_total["discount"] == Decimal("1.23")
    assert cart_total["tax"] == Decimal("2.33")
    assert cart_total["total"] == Decimal("25.60")


def test_calculate_total_handles_rounding():
    totals = calculate_total([
        {"sku": "Widget", "price": "19.99", "quantity": 3},
        {"sku": "Gadget", "price": "2.50", "quantity": 2},
    ], tax_rate=0.20, discount_rate=0.10)

    assert totals["subtotal"] == Decimal("64.97")
    assert totals["discount"] == Decimal("6.50")
    assert totals["tax"] == Decimal("11.69")
    assert totals["total"] == Decimal("70.17")


def test_quantity_validation_rejects_negative_values():
    with pytest.raises(ValueError):
        normalize_quantity(-1, minimum=1)
