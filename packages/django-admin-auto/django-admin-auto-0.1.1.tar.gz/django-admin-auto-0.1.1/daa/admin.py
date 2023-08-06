from django.contrib import admin
from django.db.models import fields

class AutoModelAdmin(admin.ModelAdmin):
    def __init__(self, model, admin_site):
        super().__init__(model,admin_site)
        fs_head=[]
        fs_tail=[]
        fs_readonly=[]
        fs_editable=[]
        fs_list_display=[]
        fs_all=self.model._meta.get_fields()
        base_dict=self.model.__bases__[0].__dict__
        for f in fs_all:
            if f.auto_created or not f.concrete: continue
            if not f.editable: fs_readonly.append(f)
            if f.name not in base_dict: fs_head.append(f)
            else: fs_tail.append(f)
        self.head_fields=tuple(f.name for f in fs_head)
        self.tail_fields=tuple(f.name for f in fs_tail)
        for f in fs_head+fs_tail:
            if f.editable: fs_editable.append(f)
            if type(f) in (fields.TextField,fields.UUIDField,fields.related.ManyToManyField): continue
            fs_list_display.append(f)
        self.auto_readonly_fields=tuple(f.name for f in fs_readonly)
        self.editable_fields=tuple(f.name for f in fs_editable)
        self.auto_list_display=tuple(f.name for f in fs_list_display)
    extra=()
    form_fields_exclude=()
    list_display_exclude=()
    queryset_Q=None
    form_field_queryset_Q=None
    def get_extra(self, request, obj=None):
        return self.extra
    def get_form_fields_exclude(self, request, obj=None):
        return self.form_fields_exclude
    def get_list_display_exclude(self, request, obj=None):
        return self.list_display_exclude
    def get_queryset_Q(self, request):
        return self.queryset_Q
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser: return qs
        q=self.get_queryset_Q(request)
        if q: qs = qs.filter(q)
        return qs.distinct()
    def get_fields(self, request, obj=None):
        form_excls=self.get_form_fields_exclude(request,obj)
        excls=self.get_exclude(request,obj)
        if excls: form_excls+=excls
        if self.fields: 
            fs=fields
        else:
            fs=self.editable_fields
            if obj: fs+=self.get_readonly_fields(request, obj)
        return tuple(f for f in fs if f not in form_excls) if form_excls else fs
    def get_readonly_fields(self, request, obj=None):
        if not obj: return ()
        if self.readonly_fields: return self.readonly_fields
        return self.auto_readonly_fields+self.get_extra(request,obj)
    def get_list_display(self, request, obj=None):
        if self.list_display[0] != '__str__': return self.list_display
        lde=self.get_list_display_exclude(request,obj)
        fs=self.auto_list_display+self.get_extra(request,obj)
        if lde: return tuple(f for f in fs if f not in lde)
        return fs
    def get_form_field_queryset_Q(self, db_field, request):
        return self.form_field_queryset_Q
    def _formfield_filter(self, db_field, request, call_back, **kwargs):
        q=self.get_form_field_queryset_Q(db_field, request)
        if q: kwargs["queryset"]=db_field.remote_field.model.objects.filter(q).distinct()
        return call_back(db_field, request, **kwargs)
    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        return self._formfield_filter(db_field, request, super().formfield_for_foreignkey, **kwargs)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        return self._formfield_filter(db_field, request, super().formfield_for_manytomany, **kwargs)