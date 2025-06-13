from django.views import View
from django.views.generic import TemplateView, DetailView
from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Account
from .models import Charge
from datetime import date, datetime

class ChargePeriodSelectView(LoginRequiredMixin, TemplateView):
    template_name = 'charges/charge_period_select.html'

    def get(self, request, *args, **kwargs):
        active = request.user.accounts.filter(is_active=True).first()
        accounts = request.user.accounts.all()
        return render(request, self.template_name, {'accounts': accounts, 'active_account': active})

    def post(self, request, *args, **kwargs):
        account_id = request.POST.get('account')
        period = request.POST.get('period')
        return redirect(f"/charges/list/?account={account_id}&period={period}")

class ChargeListView(LoginRequiredMixin, TemplateView):
    template_name = 'charges/charge_list.html'

    def get(self, request, *args, **kwargs):
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
        charges = Charge.objects.filter(account=account, period=period_date)
        total = sum(c.amount for c in charges)
        return render(request, self.template_name, {'charges': charges, 'account': account, 'period': period, 'total': total})

class ChargeDetailView(LoginRequiredMixin, DetailView):
    model = Charge
    template_name = 'charges/charge_detail.html'
    context_object_name = 'charge'

    def get_queryset(self):
        return Charge.objects.filter(account__user=self.request.user)