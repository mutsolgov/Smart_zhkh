from rest_framework import viewsets, permissions
from .models import Payment
from .serializers import PaymentSerializer
from rest_framework.exceptions import ValidationError

class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(charge_account_user=self.request.user)
    
    def perform_create(self, serializer):
        charge = serializer.validated_data['charge']
        amount = serializer.validated_data['amount']
        if charge.status == 'paid':
            raise ValidationError("Данное начисление уже оплачено")
        if amount < charge.amount:
            charge.status = 'partially_paid'
            charge.save()
        else:
            charge.status = 'paid'
            charge.save()
        serializer.save()

