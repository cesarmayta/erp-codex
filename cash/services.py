from decimal import Decimal

from django.db import transaction
from django.utils import timezone

from cash.models import CashEntry, CashSession
from core.models import AuditLog


@transaction.atomic
def open_cash_session(*, cash_register, user, opening_amount: Decimal) -> CashSession:
    if CashSession.objects.filter(cash_register=cash_register, status=CashSession.Status.OPEN).exists():
        raise ValueError("Ya existe una caja abierta para esta caja registradora.")
    session = CashSession.objects.create(
        cash_register=cash_register,
        opened_by=user,
        opening_amount=opening_amount,
        expected_amount=opening_amount,
    )
    AuditLog.objects.create(
        actor=user,
        action="cash.open",
        model_name="CashSession",
        object_id=str(session.id),
        payload={"cash_register_id": cash_register.id, "opening_amount": str(opening_amount)},
    )
    return session


@transaction.atomic
def close_cash_session(*, session: CashSession, user, closing_amount: Decimal) -> CashSession:
    if session.status != CashSession.Status.OPEN:
        raise ValueError("La caja ya esta cerrada.")
    total_income = sum(entry.amount for entry in session.entries.filter(entry_type=CashEntry.EntryType.INCOME))
    total_expense = sum(entry.amount for entry in session.entries.filter(entry_type=CashEntry.EntryType.EXPENSE))
    expected = (session.opening_amount + Decimal(total_income or 0) - Decimal(total_expense or 0)).quantize(Decimal("0.01"))
    session.expected_amount = expected
    session.closing_amount = closing_amount
    session.difference_amount = (closing_amount - expected).quantize(Decimal("0.01"))
    session.status = CashSession.Status.CLOSED
    session.closed_by = user
    session.closed_at = timezone.now()
    session.save()
    AuditLog.objects.create(
        actor=user,
        action="cash.close",
        model_name="CashSession",
        object_id=str(session.id),
        payload={"closing_amount": str(closing_amount), "difference_amount": str(session.difference_amount)},
    )
    return session
