from decimal import Decimal

from django.db import transaction

from core.models import AuditLog
from inventory.models import Product, StockMovement, StockSnapshot


def _signed_quantity(movement_type: str, quantity: Decimal) -> Decimal:
    if movement_type == StockMovement.MovementType.IN:
        return quantity
    if movement_type == StockMovement.MovementType.OUT:
        return -quantity
    return quantity


@transaction.atomic
def register_stock_movement(
    *,
    movement_type: str,
    product: Product,
    warehouse,
    quantity: Decimal,
    reference: str = "",
    notes: str = "",
    actor=None,
):
    if quantity <= 0:
        raise ValueError("La cantidad debe ser mayor a cero.")

    snapshot, _created = StockSnapshot.objects.select_for_update().get_or_create(
        product=product,
        warehouse=warehouse,
        defaults={"quantity": Decimal("0.00")},
    )
    signed_qty = _signed_quantity(movement_type, quantity)
    if movement_type == StockMovement.MovementType.OUT and snapshot.quantity < quantity:
        raise ValueError("Stock insuficiente.")

    snapshot.quantity += signed_qty
    snapshot.save(update_fields=["quantity", "updated_at"])

    movement = StockMovement.objects.create(
        movement_type=movement_type,
        product=product,
        warehouse=warehouse,
        quantity=quantity,
        unit_cost=product.cost_price,
        reference=reference,
        notes=notes,
    )
    AuditLog.objects.create(
        actor=actor,
        action=f"stock.{movement_type}",
        model_name="StockMovement",
        object_id=str(movement.id),
        payload={"product_id": product.id, "warehouse_id": warehouse.id, "quantity": str(quantity)},
    )
    return movement
