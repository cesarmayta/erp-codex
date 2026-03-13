from decimal import Decimal

from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cash.models import CashSession
from core.models import Branch, Warehouse
from inventory.models import Product
from pos.services import create_pos_sale
from sales.models import Customer, Payment


class POSOrderView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        branch = Branch.objects.get(pk=request.data["branch"])
        warehouse = Warehouse.objects.get(pk=request.data["warehouse"])
        customer = Customer.objects.get(pk=request.data["customer"])
        cash_session = CashSession.objects.get(pk=request.data["cash_session"])

        items = []
        for raw_item in request.data.get("items", []):
            items.append(
                {
                    "product": Product.objects.get(pk=raw_item["product"]),
                    "quantity": Decimal(str(raw_item["quantity"])),
                    "unit_price": Decimal(str(raw_item.get("unit_price", "0.00"))),
                    "discount_amount": Decimal(str(raw_item.get("discount_amount", "0.00"))),
                }
            )
        sale = create_pos_sale(
            branch=branch,
            warehouse=warehouse,
            customer=customer,
            seller=request.user,
            cash_session=cash_session,
            items=items,
            payment_method=request.data.get("payment_method", Payment.Method.CASH),
        )
        return Response(
            {
                "sale_id": sale.id,
                "document_number": sale.document_number,
                "total": sale.total,
                "status": sale.status,
            },
            status=status.HTTP_201_CREATED,
        )
