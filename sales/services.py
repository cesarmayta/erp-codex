from decimal import Decimal

from django.conf import settings
from django.db import transaction

from cash.models import CashEntry, CashSession
from core.models import AuditLog, BusinessSetting
from inventory.models import StockMovement
from inventory.services import register_stock_movement
from sales.models import Payment, Sale


def _tax_rate() -> Decimal:
    return BusinessSetting.get_decimal("tax_rate", Decimal(settings.ERP_DEFAULT_TAX_RATE))


def recalculate_sale(sale: Sale) -> Sale:
    subtotal = sum((line.quantity * line.unit_price) - line.discount_amount for line in sale.lines.all())
    subtotal = Decimal(subtotal or 0).quantize(Decimal("0.01"))
    tax_rate = _tax_rate() / Decimal("100")
    tax_amount = (subtotal * tax_rate).quantize(Decimal("0.01"))
    sale.subtotal = subtotal
    sale.tax_amount = tax_amount
    sale.total = (subtotal + tax_amount).quantize(Decimal("0.01"))
    sale.save(update_fields=["subtotal", "tax_amount", "total", "updated_at"])
    return sale


@transaction.atomic
def confirm_sale(sale: Sale, actor=None, cash_session: CashSession | None = None) -> Sale:
    if sale.status != Sale.Status.DRAFT:
        raise ValueError("Solo se pueden confirmar ventas en borrador.")
    if not sale.lines.exists():
        raise ValueError("La venta debe tener al menos una linea.")
    if cash_session and cash_session.status != CashSession.Status.OPEN:
        raise ValueError("La caja debe estar abierta.")

    recalculate_sale(sale)
    sale.assign_document_number()
    sale.status = Sale.Status.CONFIRMED
    sale.save(update_fields=["document_number", "status", "updated_at"])

    for line in sale.lines.select_related("product"):
        register_stock_movement(
            movement_type=StockMovement.MovementType.OUT,
            product=line.product,
            warehouse=sale.warehouse,
            quantity=line.quantity,
            reference=sale.document_number,
            notes="Salida por venta",
            actor=actor,
        )

    if cash_session:
        paid_cash = sum(payment.amount for payment in sale.payments.filter(method__in=[Payment.Method.CASH, Payment.Method.MIXED]))
        if paid_cash:
            CashEntry.objects.create(
                session=cash_session,
                entry_type=CashEntry.EntryType.INCOME,
                amount=paid_cash,
                description=f"Venta {sale.document_number}",
                sale=sale,
            )

    AuditLog.objects.create(
        actor=actor,
        action="sale.confirm",
        model_name="Sale",
        object_id=str(sale.id),
        payload={"document_number": sale.document_number, "total": str(sale.total)},
    )
    return sale


@transaction.atomic
def cancel_sale(sale: Sale, actor=None) -> Sale:
    if sale.status != Sale.Status.CONFIRMED:
        raise ValueError("Solo se pueden anular ventas confirmadas.")

    for line in sale.lines.select_related("product"):
        register_stock_movement(
            movement_type=StockMovement.MovementType.IN,
            product=line.product,
            warehouse=sale.warehouse,
            quantity=line.quantity,
            reference=sale.document_number,
            notes="Reversion por anulacion",
            actor=actor,
        )
    sale.status = Sale.Status.CANCELLED
    sale.save(update_fields=["status", "updated_at"])
    AuditLog.objects.create(
        actor=actor,
        action="sale.cancel",
        model_name="Sale",
        object_id=str(sale.id),
        payload={"document_number": sale.document_number},
    )
    return sale
