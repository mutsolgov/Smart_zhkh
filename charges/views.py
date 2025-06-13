from rest_framework import viewsets, permissions
from .models import Charge
from .serializers import ChargeSerializer
from rest_framework.exceptions import PermissionDenied
from accounts.models import Account
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status

import io
from datetime import date

from django.http import FileResponse, Http404
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas


class ChargeViewSet(viewsets.ModelViewSet):
    serializer_class = ChargeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Charge.objects.filter(account__user=self.request.user)

    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        if account.user != self.request.user:
            raise PermissionDenied("Нельзя создать начисление для чужого счёта")
        serializer.save()

    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.account.user != self.request.user:
            raise PermissionDenied("Нельзя редактировать чужое начисление")
        serializer.save()

    @action(detail=False, methods=['get'], url_path='by-period')
    def by_period(self, request):
        account_id = request.query_params.get('account')
        period = request.query_params.get('period')  # формат 'YYYY-MM'
        if not account_id or not period:
            return Response({"detail": "Укажите account и period в формате YYYY-MM"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            account = Account.objects.get(pk=account_id, user=request.user)
        except Account.DoesNotExist:
            return Response({"detail": "Счёт не найден"}, status=status.HTTP_404_NOT_FOUND)
        try:
            year, month = map(int, period.split('-'))
            period_date = date(year, month, 1)
        except:
            return Response({"detail": "Неверный формат period"}, status=status.HTTP_400_BAD_REQUEST)
        charges = Charge.objects.filter(account=account, period=period_date)
        serializer = self.get_serializer(charges, many=True)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'], url_path='receipt-period')
    def receipt_period(self, request):
        account_id = request.query_params.get('account')
        period = request.query_params.get('period')
        if not account_id or not period:
            return Response({"detail": "Укажите account и period"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            account = Account.objects.get(pk=account_id, user=request.user)
        except Account.DoesNotExist:
            return Response({"detail": "Счёт не найден"}, status=status.HTTP_404_NOT_FOUND)
        try:
            year, month = map(int, period.split('-'))
            period_date = date(year, month, 1)
        except:
            return Response({"detail": "Неверный формат period"}, status=status.HTTP_400_BAD_REQUEST)
        charges = Charge.objects.filter(account=account, period=period_date)
        if not charges:
            return Response({"detail": "Нет начислений за указанный период"}, status=status.HTTP_404_NOT_FOUND)
        # Генерация PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer, pagesize=A4)
        left_margin = 20 * mm
        top_margin = 280 * mm
        # Шапка
        p.setFont("Helvetica-Bold", 16)
        p.drawString(left_margin, top_margin, f"КВИТАНЦИЯ для счёта {account.number} за {period}")
        p.setFont("Helvetica", 10)
        created_date = date.today()
        p.drawString(left_margin, top_margin-20, f"Дата формирования: {created_date.strftime('%d.%m.%Y')}")
        user = request.user
        p.drawString(left_margin, top_margin-35, f"ФИО: {user.full_name}")
        p.drawString(left_margin, top_margin-50, f"Адрес: {account.address}")
        # Таблица
        table_top = top_margin-80
        p.setFont("Helvetica-Bold", 12)
        p.drawString(left_margin, table_top, "Услуга")
        p.drawString(left_margin+100*mm, table_top, "Сумма (₽)")
        p.setFont("Helvetica", 10)
        y = table_top-20
        total = 0
        for ch in charges:
            p.drawString(left_margin, y, ch.service.name)
            p.drawString(left_margin+100*mm, y, f"{ch.amount:.2f}")
            total += float(ch.amount)
            y -= 15
            if y < 50*mm:
                p.showPage()
                y = top_margin
        p.setFont("Helvetica-Bold", 12)
        p.drawString(left_margin, y-10, "Итого к оплате:")
        total_text = f"{total:.2f} ₽"
        text_width = p.stringWidth(total_text, "Helvetica-Bold", 12)
        p.drawString(A4[0]-left_margin-text_width, y-10, total_text)
        p.showPage()
        p.save()
        buffer.seek(0)
        filename = f"receipt_{account.number}_{period}.pdf"
        return FileResponse(buffer, as_attachment=True, filename=filename)
