from django.contrib import admin
from tools.decorators import admin_register
from wedding.seating.models import *


class SeatInline(admin.TabularInline):
    model = Seat
    

@admin_register(Table)
class TableAdmin(admin.ModelAdmin):
    inlines = (SeatInline,)
    list_display = ('label', '__len__', 'description')