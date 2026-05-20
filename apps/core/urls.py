from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('faq/', views.faq_view, name='faq'),
    path('faq/<int:faq_id>/helpful/', views.faq_helpful, name='faq_helpful'),
    path('help-support/', views.support_view, name='support'),
    path('help-support/<int:ticket_id>/', views.ticket_detail_view, name='ticket_detail'),
    path('notifications/', views.notifications_view, name='notifications'),
    path('api/notifications/', views.notifications_api, name='notifications_api'),
    path('api/notifications/mark-read/', views.mark_all_read, name='mark_all_read'),
    path('api/notifications/<int:notif_id>/delete/', views.delete_notification, name='delete_notification'),
    path('contact/', views.contact_view, name='contact'),
    path('feedback/', views.feedback_view, name='feedback'),
]
