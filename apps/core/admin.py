from django.contrib import admin
from .models import FAQCategory, FAQ, SupportTicket, SupportReply, Notification, Feedback, EmailLog, ContactMessage


@admin.register(FAQCategory)
class FAQCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'category_type', 'order']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ['question', 'category', 'is_popular', 'helpful_count', 'order']
    list_filter = ['category', 'is_popular']
    search_fields = ['question', 'answer']
    list_editable = ['is_popular', 'order']


class SupportReplyInline(admin.TabularInline):
    model = SupportReply
    extra = 1


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'user', 'issue_type', 'priority', 'status', 'created_at']
    list_filter = ['status', 'priority', 'issue_type']
    search_fields = ['title', 'user__username']
    list_editable = ['status', 'priority']
    inlines = [SupportReplyInline]


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'title', 'notif_type', 'is_read', 'created_at']
    list_filter = ['notif_type', 'is_read']
    search_fields = ['user__username', 'title']


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['name', 'emotion', 'rating', 'category', 'created_at']
    list_filter = ['emotion', 'category', 'rating']


@admin.register(EmailLog)
class EmailLogAdmin(admin.ModelAdmin):
    list_display = ['recipient', 'subject', 'event_type', 'status', 'created_at']
    list_filter = ['status', 'event_type']


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read']
