from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from inventory.api import CategoryViewSet, ProductViewSet, StockMovementViewSet, StockSnapshotViewSet
from inventory.views import ProductLookupView
from sales.api import CustomerViewSet, SaleViewSet
from cash.api import CashRegisterViewSet, CashSessionViewSet, CashEntryViewSet
from pos.api import POSOrderView
from users.forms import StyledAuthenticationForm

router = DefaultRouter()
router.register("inventory/categories", CategoryViewSet, basename="category")
router.register("inventory/products", ProductViewSet, basename="product")
router.register("inventory/movements", StockMovementViewSet, basename="stock-movement")
router.register("inventory/snapshots", StockSnapshotViewSet, basename="stock-snapshot")
router.register("sales/customers", CustomerViewSet, basename="customer")
router.register("sales/sales", SaleViewSet, basename="sale")
router.register("cash/registers", CashRegisterViewSet, basename="cash-register")
router.register("cash/sessions", CashSessionViewSet, basename="cash-session")
router.register("cash/entries", CashEntryViewSet, basename="cash-entry")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/login/", auth_views.LoginView.as_view(template_name="auth/login.html", authentication_form=StyledAuthenticationForm), name="login"),
    path("accounts/logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("api/", include(router.urls)),
    path("api/pos/orders/", POSOrderView.as_view(), name="pos-order"),
    path("api/lookup/products/", ProductLookupView.as_view(), name="product-lookup"),
    path("", include("core.urls")),
    path("inventario/", include("inventory.urls")),
    path("ventas/", include("sales.urls")),
    path("caja/", include("cash.urls")),
    path("pos/", include("pos.urls")),
]
