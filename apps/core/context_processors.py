from .models import Notification

def notifications(request):
    if request.user.is_authenticated:
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        recent_notifs = Notification.objects.filter(user=request.user)[:5]
        return {'unread_notif_count': unread_count, 'recent_notifs': recent_notifs}
    return {'unread_notif_count': 0, 'recent_notifs': []}
