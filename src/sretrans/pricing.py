from __future__ import annotations

from decimal import Decimal, ROUND_HALF_UP
from typing import Iterable, Mapping


def to_money(value: Decimal | int | float | str) -> Decimal:
    return Decimal(str(value)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


def normalize_quantity(value: int | str, minimum: int = 0) -> int:
    quantity = int(value)
    if quantity < minimum:
        raise ValueError(f"Quantity must be at least {minimum}.")
    return quantity


def calculate_subtotal(items: Iterable[Mapping[str, object]]) -> Decimal:
    subtotal = Decimal("0")
    for item in items:
        price = Decimal(str(item["price"]))
        quantity = normalize_quantity(item["quantity"], minimum=1)
        subtotal += price * quantity
    return to_money(subtotal)


def calculate_total(items: Iterable[Mapping[str, object]], tax_rate: float = 0.10, discount_rate: float = 0.0) -> dict[str, Decimal]:
    subtotal = calculate_subtotal(items)
    discount_rate_decimal = Decimal(str(discount_rate))
    tax_rate_decimal = Decimal(str(tax_rate))

    discount = subtotal * discount_rate_decimal
    taxable_subtotal = subtotal - discount
    tax = taxable_subtotal * tax_rate_decimal
    total = taxable_subtotal + tax

    return {
        "subtotal": subtotal,
        "discount": to_money(discount),
        "tax": to_money(tax),
        "total": to_money(total),
    }
