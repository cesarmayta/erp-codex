from django.core.management.base import BaseCommand

from tenancy.models import Client, Domain


class Command(BaseCommand):
    help = "Crea un tenant demo basico para desarrollo local."

    def handle(self, *args, **options):
        tenant, created = Client.objects.get_or_create(
            schema_name="demo",
            defaults={
                "name": "Demo Retail SAC",
                "slug": "demo-retail",
                "country_code": "PE",
                "currency_code": "PEN",
                "timezone": "America/Lima",
            },
        )
        Domain.objects.get_or_create(
            tenant=tenant,
            domain="demo.localhost",
            defaults={"is_primary": True},
        )
        verb = "Creado" if created else "Existente"
        self.stdout.write(self.style.SUCCESS(f"{verb}: tenant demo en schema '{tenant.schema_name}'"))
