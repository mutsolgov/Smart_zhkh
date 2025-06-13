from django.db import models
from charges.models import Charge

class Payment(models.Model):
    charge = models.ForeignKey(Charge, on_delete=models.CASCADE, related_name='payments')
    date = models.DateTimeField("Дата платежа", auto_now_add=True)
    amount = models.DecimalField("Сумма платежа", max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Платеж {self.amount} по {self.charge}"
