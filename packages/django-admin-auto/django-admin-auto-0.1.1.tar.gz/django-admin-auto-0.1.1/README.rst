===================
Example
===================

from daa.admin import AutoModelAdmin

from django.db.models import Q

from django.utils.html import format_html

class OwnershipModelAdmin(AutoModelAdmin):

    def get_queryset_Q(self, request):
        return Q(owner=request.user)

    def get_form_field_queryset_Q(self, db_field, request):
        if db_field.name=='account':
            return Q(onwer=request.user)

    def get_form_fields_exclude(self,request,obj=None):
        return () if obj else ('owner',)

    def action(self,obj):
        return format_html('<a href="url" class="button">Load</a>')

    extra=('action',)

===================
Install
===================
pip install django-admin-auto