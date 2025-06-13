from rest_framework import serializers
from .models import Charge
from accounts.models import Account
from .models import ServiceType
from django.utils.dateparse import parse_date


class ChargeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Charge
        fields = ['id', 'account', 'service', 'amount', 'period', 'status']
        read_only_fields = ['status']

    def validate(self, data):
        request = self.context['request']
        account = data.get('account')
        if account.user != request.user:
            raise serializers.ValidationError("Нельзя создать начисление для чужого счёта")
        period = data.get('period')
        return data