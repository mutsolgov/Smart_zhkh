from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['number', 'address', 'area', 'residents_count', 'managing_company', 'is_active']
        widgets = {
            'number': forms.TextInput(attrs={'pattern': '\\d{10}', 'title': '10 цифр'}),
            'address': forms.TextInput(),
            'area': forms.NumberInput(attrs={'step': '0.01', 'min': '0.01'}),
            'residents_count': forms.NumberInput(attrs={'min': '1'}),
            'managing_company': forms.TextInput(),
        }