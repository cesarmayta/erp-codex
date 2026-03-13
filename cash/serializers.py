from rest_framework import serializers

from cash.models import CashEntry, CashRegister, CashSession


class CashRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashRegister
        fields = "__all__"


class CashEntrySerializer(serializers.ModelSerializer):
    class Meta:
        model = CashEntry
        fields = "__all__"


class CashSessionSerializer(serializers.ModelSerializer):
    entries = CashEntrySerializer(many=True, read_only=True)

    class Meta:
        model = CashSession
        fields = "__all__"
