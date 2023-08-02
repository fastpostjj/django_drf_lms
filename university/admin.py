from django.contrib import admin

from university.models import  Curs, Lesson, Subscription


# Register your models here.

@admin.register(Curs)
class CursAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'preview', 'description', 'owner')
    list_display_links = ('id', 'title', 'amount', 'preview', 'description', 'owner')
    list_filter = ('id', 'title', 'amount', 'preview', 'description', 'owner')
    search_fields = ('id', 'title', 'amount', 'preview', 'description', 'owner')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'amount', 'preview','description','url_video','curs', 'owner')
    list_display_links = ('id', 'title', 'amount', 'preview','description','url_video','curs', 'owner')
    list_filter = ('id', 'title', 'amount', 'preview','description','url_video','curs', 'owner')
    search_fields = ('id', 'title', 'amount', 'preview','description','url_video','curs', 'owner')

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display =('id', 'user', 'curs') # , 'subscribed')
    list_display_links =('id', 'user', 'curs') # , 'subscribed')
    list_filter =('id', 'user', 'curs') # , 'subscribed')
    search_fields =('id', 'user', 'curs') # , 'subscribed')