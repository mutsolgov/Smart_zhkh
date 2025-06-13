from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy, reverse
from django.shortcuts import redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account
from .forms import AccountForm
from rest_framework.exceptions import PermissionDenied

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class AccountDetailView(LoginRequiredMixin, DetailView):
    model = Account
    template_name = 'accounts/account_detail.html'
    context_object_name = 'account'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class AccountCreateView(LoginRequiredMixin, CreateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account-list')

    def form_valid(self, form):
        account = form.save(commit=False)
        account.user = self.request.user
        account.owner_full_name = self.request.user.full_name
        account.save()
        return redirect(self.success_url)

class AccountUpdateView(LoginRequiredMixin, UpdateView):
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('account-list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('account-list')

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)

class AccountSetActiveView(LoginRequiredMixin, View):
    def post(self, request, pk):
        try:
            account = Account.objects.get(pk=pk, user=request.user)
        except Account.DoesNotExist:
            raise PermissionDenied("Счёт не найден или не принадлежит вам")
        account.is_active = True
        account.save()
        return redirect('account-detail', pk=pk)