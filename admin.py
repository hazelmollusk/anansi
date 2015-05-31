from django.contrib import admin
from polymorphic.admin import PolymorphicParentModelAdmin, PolymorphicChildModelAdmin
from .models import *

class TagOptionInline(admin.TabularInline):
    model = TagOption
    extra = 0

class TagAdmin(admin.ModelAdmin):
    inlines = [ TagOptionInline, ]

class VariableInline(admin.TabularInline):
    model = Variable
    fields = ('name', 'value', 'auto')
    extra = 0

class CollectorBaseAdmin(PolymorphicChildModelAdmin):
    base_model = Collector
    base_fields = ('name', 'description',)
    base_fieldsets = (
        ('Collector options', {'fields': (
            ('name',),
            ('description',),
        )}),
    )

class VMWareCollectorAdmin(CollectorBaseAdmin):
    base_model = Collector
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
    inlines = [ VariableInline, ]

class EC2CollectorAdmin(PolymorphicChildModelAdmin):
    base_model = Collector
    base_fieldsets = (
        ('Connection options', {'fields': (
            ('username', 'password'),
        )}),
        ('EC2 options', { 'fields':(('region',),) }),
        )
    inlines = [ VariableInline, ]

class StaticCollectorAdmin(PolymorphicChildModelAdmin):
    base_model = Collector
    base_fieldsets = (
        ('Connection options', {'fields': (
            ('username', 'password'),
        )}),
        ('Static options', { 'fields':(('filename',),) }),
        )
    inlines = [ VariableInline, ]

class LocalCollectorAdmin(PolymorphicChildModelAdmin):
    base_model = Collector
    base_fieldsets = (
        ('Connection options', {'fields': (
            ('username', 'password'),
            )}),
        )
    inlines = [ VariableInline, ]

## has issues with Polymorphic
# def collect_action(modeladmin, request, queryset):
#   for c in queryset:
#     c.update()
# collect_action.short_description = 'Update collections'

class CollectorParentAdmin(PolymorphicParentModelAdmin):
    base_model = Collector
    child_models = (
        (VMWareCollector, VMWareCollectorAdmin),
        (EC2Collector, EC2CollectorAdmin),
        (StaticCollector, StaticCollectorAdmin),
        (LocalCollector, LocalCollectorAdmin),
    )
#    actions = [ collect_action ]

class HostAdmin(admin.ModelAdmin):
    fields = ('name', 'source', 'auto',)
    inlines = [ VariableInline ]

admin.site.register(Collector, CollectorParentAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Host, HostAdmin)
admin.site.register(Group)
admin.site.register(VariableGroup)
admin.site.register(GroupPattern)