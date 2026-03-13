from django.urls import path

from cash.views import (
    CashEntryCreateView,
    CashEntryListView,
    CashRegisterCreateView,
    CashRegisterDeleteView,
    CashRegisterListView,
    CashRegisterUpdateView,
    CashSessionCloseView,
    CashSessionListView,
    CashSessionOpenView,
)

urlpatterns = [
    path("cajas/", CashRegisterListView.as_view(), name="cash-register-list"),
    path("cajas/nueva/", CashRegisterCreateView.as_view(), name="cash-register-create"),
    path("cajas/<int:pk>/editar/", CashRegisterUpdateView.as_view(), name="cash-register-update"),
    path("cajas/<int:pk>/eliminar/", CashRegisterDeleteView.as_view(), name="cash-register-delete"),
    path("sesiones/", CashSessionListView.as_view(), name="cash-session-list"),
    path("sesiones/abrir/", CashSessionOpenView.as_view(), name="cash-session-open"),
    path("sesiones/<int:pk>/cerrar/", CashSessionCloseView.as_view(), name="cash-session-close"),
    path("movimientos/", CashEntryListView.as_view(), name="cash-entry-list"),
    path("movimientos/nuevo/", CashEntryCreateView.as_view(), name="cash-entry-create"),
]
