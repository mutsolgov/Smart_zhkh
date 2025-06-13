from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator, MinValueValidator

class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='accounts')
    number = models.CharField("Номер лицевого счета", max_length=10, unique=True, validators=[RegexValidator(r'^\d{10}$', message="Номер должен состоять из 10 цифр")])
    address = models.CharField("Адрес помещения", max_length=255)
    owner_full_name =models.CharField("ФИО владельца", max_length=150)
    area = models.DecimalField("Площадь (м²)", max_digits=7, decimal_places=2, validators=[MinValueValidator(0.01)])
    residents_count = models.PositiveIntegerField("Количество проживающих", validators=[MinValueValidator(1)])
    managing_company = models.CharField("Управляющая компания", max_length=150)
    is_active = models.BooleanField("Активный счет", default=False)

    def save(self, *args, **kwargs):
        if self.is_active:
            Account.objects.filter(user=self.user, is_active=True).exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.number} ({self.address})"
    