from decimal import Decimal

from django.core.management import call_command
from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context

from tenancy.models import Client, Domain


class Command(BaseCommand):
    help = "Crea un tenant demo llamado empresa1 con datos minimos para pruebas."

    def handle(self, *args, **options):
        tenant, created = Client.objects.get_or_create(
            schema_name="empresa1",
            defaults={
                "name": "Empresa 1 SAC",
                "slug": "empresa1",
                "country_code": "PE",
                "currency_code": "PEN",
                "timezone": "America/Lima",
            },
        )
        Domain.objects.get_or_create(
            tenant=tenant,
            domain="empresa1.localhost",
            defaults={"is_primary": True},
        )

        # Asegura las migraciones del tenant antes de sembrar datos.
        call_command("migrate_schemas", schema_name=tenant.schema_name, interactive=False, verbosity=0)

        with schema_context(tenant.schema_name):
            from django.contrib.auth import get_user_model

            from cash.models import CashRegister
            from core.models import Branch, BusinessSetting, Warehouse
            from inventory.models import Category, Product
            from inventory.services import register_stock_movement
            from sales.models import Customer

            User = get_user_model()

            owner, owner_created = User.objects.get_or_create(
                username="admin",
                defaults={
                    "email": "admin@empresa1.localhost",
                    "role": "owner",
                    "is_staff": True,
                    "is_superuser": True,
                },
            )
            if owner_created:
                owner.set_password("admin123")
                owner.save(update_fields=["password"])

            branch, _ = Branch.objects.get_or_create(
                code="EMP1",
                defaults={"name": "Empresa 1 - Principal", "series_prefix": "T001"},
            )
            warehouse, _ = Warehouse.objects.get_or_create(
                code="ALM1",
                defaults={"name": "Almacen principal", "branch": branch},
            )
            CashRegister.objects.get_or_create(
                branch=branch,
                code="CAJA1",
                defaults={"name": "Caja principal"},
            )
            BusinessSetting.objects.get_or_create(key="tax_rate", defaults={"value": "18.00"})
            category, _ = Category.objects.get_or_create(name="General")
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

        status = "creado" if created else "actualizado"
        self.stdout.write(
            self.style.SUCCESS(
                f"Tenant {status}: schema=empresa1 domain=empresa1.localhost usuario=admin clave=admin123 cliente='{customer.name}'"
            )
        )
