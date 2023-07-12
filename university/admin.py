from django.contrib import admin

from university.models import Paying, Curs, Lesson


# Register your models here.

@admin.register(Paying)
class PayingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method')
    list_display_links = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method')
    list_filter = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method')
    search_fields = ('id', 'user', 'date_pay', 'paid_for_curs', 'paid_for_lesson', 'amount', 'payment_method')

@admin.register(Curs)
class CursAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview', 'description')
    list_display_links = ('id', 'title', 'preview', 'description')
    list_filter = ('id', 'title', 'preview', 'description')
    search_fields = ('id', 'title', 'preview', 'description')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'preview','description','url_video','curs')
    list_display_links = ('id', 'title', 'preview','description','url_video','curs')
    list_filter = ('id', 'title', 'preview','description','url_video','curs')
    search_fields = ('id', 'title', 'preview','description','url_video','curs')