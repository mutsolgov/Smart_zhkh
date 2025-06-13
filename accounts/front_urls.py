from django.urls import path
from . import html_views as account_views

urlpatterns = [
    path('', account_views.AccountListView.as_view(), name='account-list'),
    path('create/', account_views.AccountCreateView.as_view(), name='account-create'),
    path('<int:pk>/', account_views.AccountDetailView.as_view(), name='account-detail'),
    path('<int:pk>/edit/', account_views.AccountUpdateView.as_view(), name='account-edit'),
    path('<int:pk>/delete/', account_views.AccountDeleteView.as_view(), name='account-delete'),
    path('<int:pk>/set-active/', account_views.AccountSetActiveView.as_view(), name='account-set-active'),
]