from rest_framework import serializers

class InitiatePaymentInputSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()

class VerifyPaymentInputSerializer(serializers.Serializer):
    reference = serializers.CharField(max_length=100)
