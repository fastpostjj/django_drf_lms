from django.contrib import admin

from payments.models import Paying


# Register your models here.


@admin.register(Paying)
class PayingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method', 'id_intent', 'status')
    list_display_links = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method', 'id_intent', 'status')
    list_filter = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method', 'id_intent', 'status')
    search_fields = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method', 'id_intent', 'status')
