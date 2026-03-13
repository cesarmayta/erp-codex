from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cash.models import CashSession
from sales.models import Customer, Sale
from sales.serializers import CustomerSerializer, SaleSerializer
from sales.services import cancel_sale, confirm_sale


class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    search_fields = ["name", "document_number"]


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.select_related("branch", "warehouse", "customer", "seller").prefetch_related("lines", "payments").all()
    serializer_class = SaleSerializer
    filterset_fields = ["status", "branch", "warehouse", "customer"]
    search_fields = ["document_number", "customer__name"]

    @action(detail=True, methods=["post"])
    def confirm(self, request, pk=None):
        sale = self.get_object()
        cash_session_id = request.data.get("cash_session_id")
        cash_session = CashSession.objects.filter(pk=cash_session_id).first() if cash_session_id else None
        sale = confirm_sale(sale, actor=request.user, cash_session=cash_session)
        return Response(self.get_serializer(sale).data, status=status.HTTP_200_OK)

    @action(detail=True, methods=["post"])
    def cancel(self, request, pk=None):
        sale = cancel_sale(self.get_object(), actor=request.user)
        return Response(self.get_serializer(sale).data, status=status.HTTP_200_OK)
