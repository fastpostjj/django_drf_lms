from rest_framework import serializers

from payments.models import Paying
from user_auth.models import User


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

class PayingSerializers_create_payment_for_curs(serializers.ModelSerializer):
    # для вьюшки создания платежа
    class Meta:
        model = Paying
        fields = (
            # 'user',
            'id',
        )

class PayingSerializers_create_payment_methods(serializers.ModelSerializer):
    # для вьюшки создания payment_methods
    class Meta:
        model = User
        fields = (
            'email',
            'id_payment_method'
        )

class PayingSerializers_confirm_payment(serializers.ModelSerializer):
    # для вьюшки подтверждения платежа
    id = serializers.IntegerField()
    class Meta:
        model = Paying
        exclude = ('user',)
        # fields = '__all__'
        #     (
        #     'id',
        #     # 'user',
        # )
