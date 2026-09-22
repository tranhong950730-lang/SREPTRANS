from __future__ import annotations

from decimal import Decimal

from .pricing import calculate_total, normalize_quantity


class Invoice:
    @staticmethod
    def total_for(lines, tax_rate: float = 0.10, discount_rate: float = 0.0) -> dict[str, Decimal]:
        normalized_lines = []
        for line in lines:
            normalized_lines.append({
                "sku": line["sku"],
                "price": str(line["price"]),
                "quantity": normalize_quantity(line["quantity"], minimum=1),
            })
        return calculate_total(normalized_lines, tax_rate=tax_rate, discount_rate=discount_rate)
