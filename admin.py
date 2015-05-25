from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from models import *

class AnansiTagOptionInline(admin.TabularInline):
    model = AnansiTagOption
    extra = 0

class AnansiTagAdmin(admin.ModelAdmin):
    inlines = [ AnansiTagOptionInline, ]

class AnansiVariableInline(admin.TabularInline):
    model = AnansiVariable
    fields = ('name', 'value', 'auto')
    extra = 0

class AnansiCollectorBaseAdmin(PolymorphicChildModelAdmin):
    base_model = AnansiCollector
    base_fields = ('name', 'description',)
    base_fieldsets = (
        ('Collector options', {'fields': (
            ('name',),
            ('description',),
        )}),
    )

class AnansiVMWareCollectorAdmin(AnansiCollectorBaseAdmin):
    base_model = AnansiCollector
    base_fieldsets = (
        ('Connection options', {'fields': (
            ('hostname', ),
            ('username', 'password'),
        )}),
        ('VMWare options', { 'fields':(
                ('datacenter',),
                ('resource_pool','cluster',),
            ), 'classes': ('collapse',)
        }),
    )
    inlines = [ AnansiVariableInline, ]

class AnansiEC2CollectorAdmin(PolymorphicChildModelAdmin):
    base_model = AnansiCollector
    base_fieldsets = (
        ('Connection options', {'fields': (
            ('username', 'password'),
        )}),
        ('EC2 options', { 'fields':(('region',),) }),
        )
    inlines = [ AnansiVariableInline, ]

def collect_action(modeladmin, request, queryset):
  for c in queryset:
    c.collect()
collect_action.short_description = 'Update collections'

class AnansiCollectorParentAdmin(PolymorphicParentModelAdmin):
    base_model = AnansiCollector
    child_models = (
        (AnansiVMWareCollector, AnansiVMWareCollectorAdmin),
        (AnansiEC2Collector, AnansiEC2CollectorAdmin),
    )
    actions = [ collect_action ]

class AnansiHostAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Host', { 'fields':(
            ('name', 'source', 'auto'),
            ('created', 'modified'),
        )}),
    )
    inlines = [ AnansiVariableInline ]

admin.site.register(AnansiCollector, AnansiCollectorParentAdmin)
admin.site.register(AnansiTag, AnansiTagAdmin)
admin.site.register(AnansiHost, AnansiHostAdmin)
admin.site.register(AnansiGroup)
admin.site.register(AnansiVariableGroup)
admin.site.register(AnansiGroupPattern)