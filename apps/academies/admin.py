from django.contrib import admin
from .models import Academy

@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'city', 'fees', 'coach_name', 'is_active', 'created_at')
    list_filter = ('sport', 'city', 'is_active', 'created_at')
    search_fields = ('name', 'coach_name', 'location', 'city')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'sport', 'description', 'is_active')
        }),
        ('Location', {
            'fields': ('location', 'city')
        }),
        ('Pricing', {
            'fields': ('fees',)
        }),
        ('Coach Information', {
            'fields': ('coach_name', 'coach_experience')
        }),
        ('Contact Information', {
            'fields': ('phone', 'email', 'website', 'image')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
