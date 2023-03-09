from django.contrib import admin
from .models import Schema, ColumnItem


class NewColumnsAddedInline(admin.TabularInline):
    model = ColumnItem


class SchemaAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'column_separator', 'string_character', 'creation_date', 'updated',
                    'is_created']
    list_filter = ['name', 'updated', 'is_created']
    inlines = [NewColumnsAddedInline, ]


admin.site.register(Schema, SchemaAdmin,)