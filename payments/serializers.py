from rest_framework import serializers
from .models import Payment
from charges.models import Charge

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'charge', 'amount', 'date']
        read_only_fields = ['date']

    def vaalidate(self, data):
        charge = data.get('charge')
        if charge.account.user != self.context['request'].user:
            raise serializers.ValidationError("Нельзя оплатить чужое начисление")
        if data.get('amount') > charge.amount:
            raise serializers.ValidationError("Сумма оплаты превышает смму начислений")
        return data