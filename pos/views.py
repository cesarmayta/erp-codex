import json
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from cash.models import CashSession
from inventory.models import Category, Product, StockSnapshot
from pos.forms import POSCheckoutForm
from pos.services import create_pos_sale
from sales.models import Customer


@login_required
def pos_terminal(request):
    products = Product.objects.filter(is_active=True).select_related("category").order_by("name")
    categories = Category.objects.order_by("name")
    customers = Customer.objects.order_by("name")
    sessions = CashSession.objects.filter(status=CashSession.Status.OPEN).select_related("cash_register", "cash_register__branch")
    snapshots = {
        snapshot.product_id: snapshot.quantity
        for snapshot in StockSnapshot.objects.select_related("warehouse").all()
    }

    if request.method == "POST":
        form = POSCheckoutForm(request.POST)
        cart_payload = request.POST.get("cart_payload", "[]")
        try:
            raw_items = json.loads(cart_payload)
        except json.JSONDecodeError:
            raw_items = []
        if form.is_valid() and raw_items:
            items = []
            for item in raw_items:
                product = Product.objects.get(pk=item["product_id"])
                items.append(
                    {
                        "product": product,
                        "quantity": Decimal(str(item["quantity"])),
                        "unit_price": Decimal(str(item["unit_price"])),
                        "discount_amount": Decimal(str(item.get("discount_amount", "0.00"))),
                    }
                )
            sale = create_pos_sale(
                branch=form.cleaned_data["branch"],
                warehouse=form.cleaned_data["warehouse"],
                customer=form.cleaned_data["customer"],
                seller=request.user,
                cash_session=form.cleaned_data["cash_session"],
                items=items,
                payment_method=form.cleaned_data["payment_method"],
                notes=form.cleaned_data["notes"],
            )
            messages.success(request, f"Venta completada: {sale.document_number} por S/ {sale.total}")
            return redirect("pos-terminal")
        messages.error(request, "Debes completar los datos del checkout y agregar productos al carrito.")
    else:
        initial_session = sessions.first()
        form = POSCheckoutForm(
            initial={
                "branch": initial_session.cash_register.branch if initial_session else None,
                "cash_session": initial_session,
                "warehouse": initial_session.cash_register.branch.warehouses.first() if initial_session else None,
                "customer": customers.filter(is_generic=True).first() or customers.first(),
            }
        )

    return render(
        request,
        "pos/terminal.html",
        {
            "products": products,
            "categories": categories,
            "customers": customers,
            "sessions": sessions,
            "snapshots": snapshots,
            "form": form,
        },
    )
