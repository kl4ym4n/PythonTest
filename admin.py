from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User


# Register your models here.
from .split_models import Link

UserAdmin.list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'date_joined', 'is_staff')
admin.site.unregister(User)
admin.site.register(User, UserAdmin)


class LinkAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'link_title', 'link', 'creation_date', 'private_flag')
    list_filter = ['creation_date']
    search_fields = ['link']

admin.site.register(Link, LinkAdmin)