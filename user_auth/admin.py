from django.contrib import admin

from user_auth.models import User


# Register your models here.

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email','phone','avatar','country', 'id_payment_method')
    list_display_links = ('id', 'email','phone','avatar','country')
    list_filter = ('id', 'email','phone','avatar','country')
    search_fields = ('id', 'email','phone','avatar','country', 'id_payment_method')
