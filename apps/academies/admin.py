from django.contrib import admin

from .models import (
    Academy,
    APIKey,
    Booking,
    ChatRoom,
    Coach,
    FavoriteAcademy,
    Message,
    UserActivity,
)


@admin.register(APIKey)
class APIKeyAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'is_active', 'created_at', 'last_used_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'user__username')
    readonly_fields = ('key', 'created_at', 'last_used_at')

    fieldsets = (
        ('API Key Information', {'fields': ('name', 'user', 'is_active')}),
        (
            'Key Details (Read-only)',
            {'fields': ('key',), 'description': 'Hashed key; raw key shown once when generated.'},
        ),
        ('Timestamps', {'fields': ('created_at', 'last_used_at'), 'classes': ('collapse',)}),
    )


@admin.register(Academy)
class AcademyAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'city', 'fees', 'rating', 'owner', 'coach_name', 'is_active', 'created_at')
    list_filter = ('sport', 'city', 'is_active', 'created_at')
    search_fields = ('name', 'coach_name', 'location', 'city')
    list_editable = ('is_active',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {'fields': ('name', 'sport', 'description', 'is_active', 'owner')}),
        ('Location & Map', {'fields': ('location', 'city', 'latitude', 'longitude')}),
        ('Pricing & Quality', {'fields': ('fees', 'rating')}),
        ('Coach Information', {'fields': ('coach_name', 'coach_experience', 'total_coaches')}),
        ('Facilities & Hours', {'fields': ('facilities', 'opening_hours')}),
        ('Contact Information', {'fields': ('phone', 'email', 'website', 'image')}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('activity', 'user', 'query', 'sport', 'city', 'academy', 'created_at')
    list_filter = ('activity', 'sport', 'created_at')
    search_fields = ('query', 'city', 'session_key')
    date_hierarchy = 'created_at'


@admin.register(FavoriteAcademy)
class FavoriteAcademyAdmin(admin.ModelAdmin):
    list_display = ('user', 'academy', 'created_at')
    search_fields = ('user__username', 'academy__name')


class MessageInline(admin.TabularInline):
    model = Message
    extra = 0
    readonly_fields = ('sender', 'body', 'created_at', 'read_at')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('academy', 'learner', 'updated_at')
    search_fields = ('academy__name', 'learner__username')
    inlines = [MessageInline]


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('room', 'sender', 'body', 'created_at', 'read_at')
    search_fields = ('body',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'academy', 'booking_date', 'status', 'created_at')
    list_filter = ('status', 'created_at')


@admin.register(Coach)
class CoachAdmin(admin.ModelAdmin):
    list_display = ('name', 'sport', 'experience', 'created_at')
