from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import EmailLog, Notification


def _send(recipient, subject, event_type, html_message, plain_message=''):
    log = EmailLog.objects.create(recipient=recipient, subject=subject, event_type=event_type)
    try:
        send_mail(
            subject=subject,
            message=plain_message or 'Please view this email in an HTML-capable client.',
            from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@sportsarena.com'),
            recipient_list=[recipient],
            html_message=html_message,
            fail_silently=False,
        )
        log.status = 'sent'
    except Exception as e:
        log.status = 'failed'
        log.error_message = str(e)
    log.save()


def send_welcome_email(user):
    html = f"""
    <div style="font-family:sans-serif;background:#0f172a;color:#fff;padding:40px;border-radius:12px;">
        <h1 style="color:#3b82f6;">Welcome to SPORTS ARENA 🏆</h1>
        <p>Hi <strong>{user.username}</strong>, your account is ready!</p>
        <p style="color:#94a3b8;">Discover world-class sports academies, connect with coaches, and start your journey.</p>
        <a href="{getattr(settings,'SITE_URL','http://127.0.0.1:8000')}/explore/" style="background:#3b82f6;color:#fff;padding:12px 24px;border-radius:8px;text-decoration:none;display:inline-block;margin-top:16px;">Explore Academies →</a>
    </div>
    """
    _send(user.email, 'Welcome to SPORTS ARENA! 🏆', 'welcome', html)
    push_notification(user, 'Welcome to SPORTS ARENA! 🏆', 'Your account is ready. Start exploring academies.', 'welcome', '/explore/')


def send_booking_confirmation(booking):
    user = booking.user
    html = f"""
    <div style="font-family:sans-serif;background:#0f172a;color:#fff;padding:40px;border-radius:12px;">
        <h1 style="color:#22c55e;">Booking Confirmed ✅</h1>
        <p>Hi <strong>{user.username}</strong>,</p>
        <p>Your booking for <strong>{booking.academy.name}</strong> on <strong>{booking.booking_date}</strong> has been received.</p>
        <p style="color:#94a3b8;">Status: <span style="color:#f59e0b;">Pending Approval</span></p>
    </div>
    """
    _send(user.email, f'Booking Confirmed — {booking.academy.name}', 'booking_confirmation', html)
    push_notification(user, 'Booking Received', f'Your booking for {booking.academy.name} is pending approval.', 'new_booking', '/accounts/dashboard/my-bookings/')


def send_booking_status_email(booking):
    user = booking.user
    color = '#22c55e' if booking.status == 'approved' else '#ef4444'
    html = f"""
    <div style="font-family:sans-serif;background:#0f172a;color:#fff;padding:40px;border-radius:12px;">
        <h1 style="color:{color};">Booking {booking.status.title()}</h1>
        <p>Hi <strong>{user.username}</strong>,</p>
        <p>Your booking for <strong>{booking.academy.name}</strong> has been <strong>{booking.status}</strong>.</p>
    </div>
    """
    event = f'booking_{booking.status}'
    _send(user.email, f'Booking {booking.status.title()} — {booking.academy.name}', event, html)
    notif_type = 'booking_approved' if booking.status == 'approved' else 'booking_rejected'
    push_notification(user, f'Booking {booking.status.title()}', f'Your booking for {booking.academy.name} was {booking.status}.', notif_type, '/accounts/dashboard/my-bookings/')


def send_ticket_created_email(ticket):
    html = f"""
    <div style="font-family:sans-serif;background:#0f172a;color:#fff;padding:40px;border-radius:12px;">
        <h1 style="color:#3b82f6;">Support Ticket Created 🎫</h1>
        <p>Hi <strong>{ticket.user.username}</strong>,</p>
        <p>Ticket <strong>#{ticket.id}</strong>: <em>{ticket.title}</em> has been created.</p>
        <p style="color:#94a3b8;">We'll respond within 24 hours.</p>
    </div>
    """
    _send(ticket.user.email, f'Support Ticket #{ticket.id} Created', 'ticket_created', html)
    push_notification(ticket.user, f'Ticket #{ticket.id} Created', 'We received your support request and will respond soon.', 'ticket_created', '/help-support/')


def send_ticket_reply_email(reply):
    ticket = reply.ticket
    html = f"""
    <div style="font-family:sans-serif;background:#0f172a;color:#fff;padding:40px;border-radius:12px;">
        <h1 style="color:#06b6d4;">New Reply on Ticket #{ticket.id} 💬</h1>
        <p>Hi <strong>{ticket.user.username}</strong>,</p>
        <p>There's a new reply on your ticket: <em>{ticket.title}</em></p>
        <blockquote style="border-left:3px solid #3b82f6;padding-left:16px;color:#94a3b8;">{reply.message[:200]}</blockquote>
    </div>
    """
    _send(ticket.user.email, f'New Reply — Ticket #{ticket.id}', 'ticket_reply', html)
    push_notification(ticket.user, f'Reply on Ticket #{ticket.id}', reply.message[:100], 'ticket_reply', '/help-support/')


def push_notification(user, title, message, notif_type='system', link=''):
    Notification.objects.create(user=user, title=title, message=message, notif_type=notif_type, link=link)
