from decimal import Decimal

from cash.models import CashSession
from core.models import BusinessSetting
from sales.models import Payment, Sale, SaleLine
from sales.services import confirm_sale


def create_pos_sale(*, branch, warehouse, customer, seller, cash_session: CashSession, items: list[dict], payment_method: str, notes: str = ""):
    if cash_session.status != CashSession.Status.OPEN:
        raise ValueError("La caja debe estar abierta.")
    sale = Sale.objects.create(
        branch=branch,
        warehouse=warehouse,
        customer=customer,
        seller=seller,
        notes=notes or "Venta POS",
    )
    for item in items:
        SaleLine.objects.create(
            sale=sale,
            product=item["product"],
            quantity=Decimal(item["quantity"]),
            unit_price=Decimal(item.get("unit_price") or item["product"].sale_price),
            discount_amount=Decimal(item.get("discount_amount", "0.00")),
            line_total=Decimal("0.00"),
        )
    subtotal = sum(
        (Decimal(item["quantity"]) * Decimal(item.get("unit_price") or item["product"].sale_price)) - Decimal(item.get("discount_amount", "0.00"))
        for item in items
    )
    tax_rate = BusinessSetting.get_decimal("tax_rate", Decimal("18.00")) / Decimal("100")
    total = (subtotal + (subtotal * tax_rate)).quantize(Decimal("0.01"))
    Payment.objects.create(
        sale=sale,
        method=payment_method,
        amount=total,
    )
    return confirm_sale(sale, actor=seller, cash_session=cash_session)
