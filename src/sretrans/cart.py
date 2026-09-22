from __future__ import annotations

from decimal import Decimal

from .pricing import calculate_total, normalize_quantity


class Cart:
    def __init__(self, items=None):
        self.items = list(items or [])

    def add_item(self, sku: str, price: Decimal | str | float, quantity: int | str = 1) -> None:
        self.items.append({
            "sku": sku,
            "price": str(price),
            "quantity": normalize_quantity(quantity, minimum=1),
        })

    def totals(self, tax_rate: float = 0.10, discount_rate: float = 0.0) -> dict[str, Decimal]:
        return calculate_total(self.items, tax_rate=tax_rate, discount_rate=discount_rate)
