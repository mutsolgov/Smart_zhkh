from django.views import View
from django.views.generic import FormView, ListView
from django.shortcuts import redirect, render
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Account
from charges.models import Charge
from .models import Payment
from .forms import PaymentForm
from django.urls import reverse
from datetime import date
from rest_framework.exceptions import PermissionDenied
from rest_framework.test import APIClient

class PayPeriodView(LoginRequiredMixin, View):
    def get(self, request):
        account_id = request.GET.get('account')
        period = request.GET.get('period')
        try:
            account = Account.objects.get(pk=account_id, user=request.user)
        except:
            return redirect('charge-period-select')
        try:
            year, month = map(int, period.split('-'))
            period_date = date(year, month, 1)
        except:
            return redirect('charge-period-select')
        charges = Charge.objects.filter(account=account, period=period_date).exclude(status='paid')
        if not charges:
            return redirect('charge-list')
        total = sum(c.amount for c in charges)
        return render(request, 'payments/pay_period_confirm.html', {'account': account, 'period': period, 'total': total})

    def post(self, request):
        account_id = request.POST.get('account')
        period = request.POST.get('period')
        try:
            account = Account.objects.get(pk=account_id, user=request.user)
        except:
            raise PermissionDenied
        year, month = map(int, period.split('-'))
        period_date = date(year, month, 1)
        charges = Charge.objects.filter(account=account, period=period_date).exclude(status='paid')

        for ch in charges:
            Payment.objects.create(charge=ch, amount=ch.amount)
            ch.status = 'paid'
            ch.save()
        return redirect('charge-list')

class PaymentCreateView(LoginRequiredMixin, FormView):
    template_name = 'payments/payment_form.html'
    form_class = PaymentForm

    def dispatch(self, request, *args, **kwargs):
        self.charge_id = kwargs.get('charge_id')
        try:
            self.charge = Charge.objects.get(pk=self.charge_id, account__user=request.user)
        except:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['charge'] = self.charge
        return context

    def form_valid(self, form):
        amount = form.cleaned_data['amount']
        if amount > self.charge.amount:
            form.add_error('amount', 'Сумма превышает начисление')
            return self.form_invalid(form)
        Payment.objects.create(charge=self.charge, amount=amount)
        if amount < self.charge.amount:
            self.charge.status = 'partial'
        else:
            self.charge.status = 'paid'
        self.charge.save()
        return redirect('charge-detail', pk=self.charge.id)

class PaymentListView(LoginRequiredMixin, ListView):
    model = Payment
    template_name = 'payments/payment_list.html'
    context_object_name = 'payments'

    def get_queryset(self):
        charge_id = self.request.GET.get('charge')
        qs = Payment.objects.filter(charge__account__user=self.request.user)
        if charge_id:
            qs = qs.filter(charge_id=charge_id)
        return qs
