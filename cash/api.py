from decimal import Decimal

from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from cash.models import CashEntry, CashRegister, CashSession
from cash.serializers import CashEntrySerializer, CashRegisterSerializer, CashSessionSerializer
from cash.services import close_cash_session, open_cash_session


class CashRegisterViewSet(viewsets.ModelViewSet):
    queryset = CashRegister.objects.select_related("branch").all()
    serializer_class = CashRegisterSerializer
    filterset_fields = ["branch", "is_active"]


class CashEntryViewSet(viewsets.ModelViewSet):
    queryset = CashEntry.objects.select_related("session", "sale").all()
    serializer_class = CashEntrySerializer
    filterset_fields = ["session", "entry_type"]


class CashSessionViewSet(viewsets.ModelViewSet):
    queryset = CashSession.objects.select_related("cash_register", "opened_by", "closed_by").prefetch_related("entries").all()
    serializer_class = CashSessionSerializer
    filterset_fields = ["cash_register", "status"]

    def create(self, request, *args, **kwargs):
        cash_register = CashRegister.objects.get(pk=request.data["cash_register"])
        session = open_cash_session(
            cash_register=cash_register,
            user=request.user,
            opening_amount=Decimal(request.data.get("opening_amount", "0.00")),
        )
        return Response(self.get_serializer(session).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=["post"])
    def close(self, request, pk=None):
        session = close_cash_session(
            session=self.get_object(),
            user=request.user,
            closing_amount=Decimal(request.data.get("closing_amount", "0.00")),
        )
        return Response(self.get_serializer(session).data, status=status.HTTP_200_OK)
