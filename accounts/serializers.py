from rest_framework import serializers
from .models import Account

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'number', 'address', 'owner_full_name', 'area', 'residents_count', 'managing_company', 'is_active']
        read_only_fields = ['owner_full_name']
    
    def validate_number(self, value):
        return value
    
    def validate(self, data):
        return data
    
    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['owner_full_name'] = user.full_name
        account = Account.objects.create(user=user, **validated_data)
        return account
    
    def update(self, instance, validated_data):
        return super().update(instance, validated_data)
