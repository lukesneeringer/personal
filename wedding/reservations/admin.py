from django.contrib import admin
from tools.decorators import admin_register
from wedding.reservations.models import *


class InviteeInline(admin.TabularInline):
    model = Invitee


@admin_register(Invitation)
class InvitationAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'address', 'city', 'state', 'zip_code')
    inlines = (InviteeInline,)
    
    
@admin_register(Gift)
class GiftAdmin(admin.ModelAdmin):
    list_display = ('invitation', 'label')
    
    
@admin_register(RSVP)
class RSVPAdmin(admin.ModelAdmin):
    list_display = ('invitee', 'accepts', 'food', 'medium', 'modified')