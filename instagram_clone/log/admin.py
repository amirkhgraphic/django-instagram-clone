from django.contrib import admin

from log.models import Log
from utils.admin.mixins import DateListFilterMixin


@admin.register(Log)
class PostAdmin(admin.ModelAdmin, DateListFilterMixin):
    list_display = ('action', 'operation', 'created_at')
    list_filter = ('operation', ) + DateListFilterMixin.list_filter
