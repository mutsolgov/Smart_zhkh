from django import forms
from .models import Payment

class PaymentForm(forms.Form):
    amount = forms.DecimalField(label='Сумма оплаты', max_digits=10, decimal_places=2, min_value=0.01)