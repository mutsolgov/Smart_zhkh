from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterForm(UserCreationForm):
    full_name = forms.CharField(label='ФИО', max_length=150)
    address = forms.CharField(label='Адрес', max_length=255)

    class Meta:
        model = User
        fields = ['username', 'full_name', 'address', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.full_name = self.cleaned_data['full_name']
        user.address = self.cleaned_data['address']
        if commit:
            user.save()
        return user
