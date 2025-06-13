from django.urls import path
from . import html_views

urlpatterns = [
    path('pay-period/', html_views.PayPeriodView.as_view(), name='payment-pay-period'),
    path('create/<int:charge_id>/', html_views.PaymentCreateView.as_view(), name='payment-create'),
    path('', html_views.PaymentListView.as_view(), name='payment-list'),
]