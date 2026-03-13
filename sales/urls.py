from django.urls import path

from sales.views import CustomerCreateView, CustomerDeleteView, CustomerListView, CustomerUpdateView, SaleListView

urlpatterns = [
    path("clientes/", CustomerListView.as_view(), name="customer-list"),
    path("clientes/nuevo/", CustomerCreateView.as_view(), name="customer-create"),
    path("clientes/<int:pk>/editar/", CustomerUpdateView.as_view(), name="customer-update"),
    path("clientes/<int:pk>/eliminar/", CustomerDeleteView.as_view(), name="customer-delete"),
    path("ventas/", SaleListView.as_view(), name="sale-list"),
]
