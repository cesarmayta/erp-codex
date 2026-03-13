from django.urls import path

from core.views import (
    BranchCreateView,
    BranchDeleteView,
    BranchListView,
    BranchUpdateView,
    BusinessSettingCreateView,
    BusinessSettingDeleteView,
    BusinessSettingListView,
    BusinessSettingUpdateView,
    CompanyUpdateView,
    DashboardView,
    WarehouseCreateView,
    WarehouseDeleteView,
    WarehouseListView,
    WarehouseUpdateView,
)

urlpatterns = [
    path("", DashboardView.as_view(), name="dashboard"),
    path("empresa/", CompanyUpdateView.as_view(), name="company-edit"),
    path("sucursales/", BranchListView.as_view(), name="branch-list"),
    path("sucursales/nuevo/", BranchCreateView.as_view(), name="branch-create"),
    path("sucursales/<int:pk>/editar/", BranchUpdateView.as_view(), name="branch-update"),
    path("sucursales/<int:pk>/eliminar/", BranchDeleteView.as_view(), name="branch-delete"),
    path("almacenes/", WarehouseListView.as_view(), name="warehouse-list"),
    path("almacenes/nuevo/", WarehouseCreateView.as_view(), name="warehouse-create"),
    path("almacenes/<int:pk>/editar/", WarehouseUpdateView.as_view(), name="warehouse-update"),
    path("almacenes/<int:pk>/eliminar/", WarehouseDeleteView.as_view(), name="warehouse-delete"),
    path("parametros/", BusinessSettingListView.as_view(), name="setting-list"),
    path("parametros/nuevo/", BusinessSettingCreateView.as_view(), name="setting-create"),
    path("parametros/<int:pk>/editar/", BusinessSettingUpdateView.as_view(), name="setting-update"),
    path("parametros/<int:pk>/eliminar/", BusinessSettingDeleteView.as_view(), name="setting-delete"),
]
