from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from cash.models import CashRegister
from core.models import Branch, BusinessSetting, Company, Warehouse
from inventory.models import Category, Product
from inventory.services import register_stock_movement
from sales.models import Customer


class Command(BaseCommand):
    help = "Crea datos demo de una sola empresa llamada Empresa 1."

    def handle(self, *args, **options):
        User = get_user_model()
        company, _ = Company.objects.get_or_create(
            business_name="Empresa 1 SAC",
            defaults={"trade_name": "Empresa 1", "currency_code": "PEN", "timezone": "America/Lima"},
        )
        owner, created = User.objects.get_or_create(
            username="admin",
            defaults={"email": "admin@empresa1.local", "role": "owner", "is_staff": True, "is_superuser": True},
        )
        if created:
            owner.set_password("admin123")
            owner.save(update_fields=["password"])
        branch, _ = Branch.objects.get_or_create(code="MAIN", defaults={"name": "Sucursal principal", "series_prefix": "T001"})
        warehouse, _ = Warehouse.objects.get_or_create(
            code="ALM1",
            defaults={"name": "Almacen principal", "branch": branch},
        )
        CashRegister.objects.get_or_create(branch=branch, code="CAJA1", defaults={"name": "Caja principal"})
        BusinessSetting.objects.get_or_create(key="tax_rate", defaults={"value": "18.00"})
        category, _ = Category.objects.get_or_create(name="Clasicos")
        customer, _ = Customer.objects.get_or_create(name="Cliente general", defaults={"is_generic": True})
        product, product_created = Product.objects.get_or_create(
            sku="P001",
            defaults={
                "name": "Producto demo",
                "category": category,
                "cost_price": Decimal("10.00"),
                "sale_price": Decimal("15.00"),
                "low_stock_threshold": Decimal("2.00"),
            },
        )
        if product_created:
            register_stock_movement(
                movement_type="in",
                product=product,
                warehouse=warehouse,
                quantity=Decimal("25.00"),
                reference="seed-empresa1",
                notes="Stock inicial demo",
                actor=owner,
            )
        self.stdout.write(
            self.style.SUCCESS(
                f"Empresa demo lista: {company.business_name} usuario=admin clave=admin123 cliente='{customer.name}'"
            )
        )
