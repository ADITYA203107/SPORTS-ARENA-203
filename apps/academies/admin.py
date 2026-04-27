from django.contrib import admin
from .models import Academy, APIKey, Booking, Coach


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'created_at', 'last_used_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('key', 'created_at', 'last_used_at')
    
    fieldsets = (
        ('API Key Information', {
            'fields': ('name', 'user', 'is_active')
        }),
        ('Key Details (Read-only)', {
            'fields': ('key',),
            'description': 'This is the hashed key. The raw key is only shown once when generated.'
        }),
        ('Timestamps', {
            'fields': ('created_at', 'last_used_at'),
            'classes': ('collapse',)
        }),
    )


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
