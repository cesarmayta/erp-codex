from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, FormView, ListView, UpdateView

from cash.forms import CashCloseForm, CashEntryForm, CashOpenForm, CashRegisterForm
from cash.models import CashEntry, CashRegister, CashSession
from cash.services import close_cash_session, open_cash_session
from core.views import CRUDListView


class CashRegisterListView(CRUDListView):
    model = CashRegister
    title = "Cajas"
    create_url = "cash-register-create"
    update_url_name = "cash-register-update"
    delete_url_name = "cash-register-delete"
    fields = ["branch", "code", "name", "is_active"]
    field_labels = {"branch": "Sucursal", "code": "Codigo", "name": "Nombre", "is_active": "Activo"}


class CashRegisterCreateView(LoginRequiredMixin, CreateView):
    model = CashRegister
    form_class = CashRegisterForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("cash-register-list")

    def form_valid(self, form):
        messages.success(self.request, "Caja creada correctamente.")
        return super().form_valid(form)


class CashRegisterUpdateView(LoginRequiredMixin, UpdateView):
    model = CashRegister
    form_class = CashRegisterForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("cash-register-list")

    def form_valid(self, form):
        messages.success(self.request, "Caja actualizada correctamente.")
        return super().form_valid(form)


class CashRegisterDeleteView(LoginRequiredMixin, DeleteView):
    model = CashRegister
    template_name = "crud/confirm_delete.html"
    success_url = reverse_lazy("cash-register-list")


class CashSessionListView(LoginRequiredMixin, ListView):
    model = CashSession
    template_name = "cash/session_list.html"
    context_object_name = "sessions"

    def get_queryset(self):
        return CashSession.objects.select_related("cash_register", "opened_by", "closed_by").order_by("-opened_at")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["open_form"] = CashOpenForm()
        return context


class CashSessionOpenView(LoginRequiredMixin, FormView):
    form_class = CashOpenForm
    http_method_names = ["post"]

    def form_valid(self, form):
        open_cash_session(
            cash_register=form.cleaned_data["cash_register"],
            user=self.request.user,
            opening_amount=form.cleaned_data["opening_amount"],
        )
        messages.success(self.request, "Caja abierta correctamente.")
        return redirect("cash-session-list")


class CashSessionCloseView(LoginRequiredMixin, FormView):
    form_class = CashCloseForm
    http_method_names = ["post"]

    def form_valid(self, form):
        session = get_object_or_404(CashSession, pk=self.kwargs["pk"])
        close_cash_session(session=session, user=self.request.user, closing_amount=form.cleaned_data["closing_amount"])
        messages.success(self.request, "Caja cerrada correctamente.")
        return redirect("cash-session-list")


class CashEntryListView(LoginRequiredMixin, ListView):
    model = CashEntry
    template_name = "cash/entry_list.html"
    context_object_name = "entries"

    def get_queryset(self):
        return CashEntry.objects.select_related("session", "sale").order_by("-created_at")[:100]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = CashEntryForm()
        return context


class CashEntryCreateView(LoginRequiredMixin, CreateView):
    model = CashEntry
    form_class = CashEntryForm
    template_name = "crud/form.html"
    success_url = reverse_lazy("cash-entry-list")

    def form_valid(self, form):
        messages.success(self.request, "Movimiento de caja registrado.")
        return super().form_valid(form)
