from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase

from cash.services import close_cash_session, open_cash_session
from core.models import Branch, Warehouse
from inventory.models import Product, StockSnapshot
from inventory.services import register_stock_movement
from sales.models import Customer, Payment, Sale, SaleLine
from sales.services import confirm_sale, cancel_sale


class WorkflowTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username="owner", password="secret", role="owner")
        self.branch = Branch.objects.create(code="LIM001", name="Principal", series_prefix="T001")
        self.warehouse = Warehouse.objects.create(code="ALM001", name="Almacen principal", branch=self.branch)
        self.customer = Customer.objects.create(name="Cliente generico", is_generic=True)
        self.product = Product.objects.create(sku="SKU-1", name="Arroz", cost_price=Decimal("3.50"), sale_price=Decimal("5.00"))

    def test_stock_in_and_out(self):
        register_stock_movement(
            movement_type="in",
            product=self.product,
            warehouse=self.warehouse,
            quantity=Decimal("10.00"),
        )
        snapshot = StockSnapshot.objects.get(product=self.product, warehouse=self.warehouse)
        self.assertEqual(snapshot.quantity, Decimal("10.00"))

    def test_confirm_sale_updates_stock(self):
        register_stock_movement(
            movement_type="in",
            product=self.product,
            warehouse=self.warehouse,
            quantity=Decimal("10.00"),
        )
        sale = Sale.objects.create(branch=self.branch, warehouse=self.warehouse, customer=self.customer, seller=self.user)
        SaleLine.objects.create(sale=sale, product=self.product, quantity=Decimal("2.00"), unit_price=Decimal("5.00"), line_total=Decimal("10.00"))
        Payment.objects.create(sale=sale, method=Payment.Method.CASH, amount=Decimal("11.80"))
        sale = confirm_sale(sale, actor=self.user)
        snapshot = StockSnapshot.objects.get(product=self.product, warehouse=self.warehouse)
        self.assertEqual(sale.status, Sale.Status.CONFIRMED)
        self.assertEqual(snapshot.quantity, Decimal("8.00"))

    def test_cash_close_computes_difference(self):
        cash_register = self.branch.cash_registers.create(code="CAJA1", name="Caja 1")
        session = open_cash_session(cash_register=cash_register, user=self.user, opening_amount=Decimal("100.00"))
        session.entries.create(entry_type="income", amount=Decimal("20.00"), description="Ingreso")
        closed = close_cash_session(session=session, user=self.user, closing_amount=Decimal("119.00"))
        self.assertEqual(closed.expected_amount, Decimal("120.00"))
        self.assertEqual(closed.difference_amount, Decimal("-1.00"))

    def test_cancel_sale_restores_stock(self):
        register_stock_movement(
            movement_type="in",
            product=self.product,
            warehouse=self.warehouse,
            quantity=Decimal("10.00"),
        )
        sale = Sale.objects.create(branch=self.branch, warehouse=self.warehouse, customer=self.customer, seller=self.user)
        SaleLine.objects.create(sale=sale, product=self.product, quantity=Decimal("2.00"), unit_price=Decimal("5.00"), line_total=Decimal("10.00"))
        Payment.objects.create(sale=sale, method=Payment.Method.CASH, amount=Decimal("11.80"))
        confirm_sale(sale, actor=self.user)
        cancel_sale(sale, actor=self.user)
        snapshot = StockSnapshot.objects.get(product=self.product, warehouse=self.warehouse)
        self.assertEqual(snapshot.quantity, Decimal("10.00"))
