from rest_framework import serializers

from sales.models import Customer, Payment, Sale, SaleLine
from sales.services import recalculate_sale


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"


class SaleLineSerializer(serializers.ModelSerializer):
    class Meta:
        model = SaleLine
        fields = ["id", "product", "quantity", "unit_price", "discount_amount", "line_total"]

    def validate(self, attrs):
        attrs["line_total"] = (attrs["quantity"] * attrs["unit_price"]) - attrs.get("discount_amount", 0)
        return attrs


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "method", "amount", "reference"]


class SaleSerializer(serializers.ModelSerializer):
    lines = SaleLineSerializer(many=True)
    payments = PaymentSerializer(many=True, required=False)

    class Meta:
        model = Sale
        fields = [
            "id",
            "branch",
            "warehouse",
            "customer",
            "seller",
            "status",
            "document_number",
            "subtotal",
            "tax_amount",
            "total",
            "notes",
            "lines",
            "payments",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["subtotal", "tax_amount", "total", "document_number", "status"]

    def create(self, validated_data):
        lines_data = validated_data.pop("lines", [])
        payments_data = validated_data.pop("payments", [])
        sale = Sale.objects.create(**validated_data)
        for line_data in lines_data:
            SaleLine.objects.create(sale=sale, **line_data)
        for payment_data in payments_data:
            Payment.objects.create(sale=sale, **payment_data)
        return recalculate_sale(sale)

    def update(self, instance, validated_data):
        lines_data = validated_data.pop("lines", None)
        payments_data = validated_data.pop("payments", None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if lines_data is not None:
            instance.lines.all().delete()
            for line_data in lines_data:
                SaleLine.objects.create(sale=instance, **line_data)
        if payments_data is not None:
            instance.payments.all().delete()
            for payment_data in payments_data:
                Payment.objects.create(sale=instance, **payment_data)
        return recalculate_sale(instance)
