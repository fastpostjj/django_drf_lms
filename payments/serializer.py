from rest_framework import serializers

from payments.models import Paying


class PayingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Paying
        fields = (
            'user',
            'date_pay',
            'paid_for_curs',
            'paid_for_lesson',
            'amount',
            'payment_method',
            'id_intent',
            'status'
        )