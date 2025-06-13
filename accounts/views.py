from django.shortcuts import render
from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from .serializers import AccountSerializer
from rest_framework.exceptions import PermissionDenied


class AccountViewSet(viewsets.ModelViewSet):
    serializer_class = AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.user != self.request.user:
            raise PermissionDenied("Нельзя редактировать чужой счет")
        serializer.save()

    @action(detail=True, methods=['post'], url_path='set-active')
    def set_active(self, request, pk=None):
        account = self.get_object()
        if account.user != request.user:
            raise PermissionDenied("Нельзя выбрать чужой счет")
        account.is_active = True
        account.save()
        return Response({'status': 'активный счет установлен'})
    