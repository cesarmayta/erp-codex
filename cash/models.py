from decimal import Decimal

from django.conf import settings
from django.db import models

from core.models import Branch, TimeStampedModel


class CashRegister(TimeStampedModel):
    branch = models.ForeignKey(Branch, on_delete=models.PROTECT, related_name="cash_registers")
    code = models.CharField(max_length=20)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ("branch", "code")

    def __str__(self) -> str:
        return f"{self.branch.code}-{self.code}"


class CashSession(TimeStampedModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        CLOSED = "closed", "Closed"

    cash_register = models.ForeignKey(CashRegister, on_delete=models.PROTECT, related_name="sessions")
    opened_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="opened_cash_sessions")
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.PROTECT,
        related_name="closed_cash_sessions",
    )
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    opening_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    closing_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    expected_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    difference_amount = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    opened_at = models.DateTimeField(auto_now_add=True)
    closed_at = models.DateTimeField(null=True, blank=True)


class CashEntry(TimeStampedModel):
    class EntryType(models.TextChoices):
        INCOME = "income", "Income"
        EXPENSE = "expense", "Expense"

    session = models.ForeignKey(CashSession, on_delete=models.CASCADE, related_name="entries")
    entry_type = models.CharField(max_length=10, choices=EntryType.choices)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.CharField(max_length=255)
    sale = models.ForeignKey("sales.Sale", null=True, blank=True, on_delete=models.SET_NULL, related_name="cash_entries")
