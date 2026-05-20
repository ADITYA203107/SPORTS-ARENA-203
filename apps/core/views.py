from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Avg, Count, Q
from .models import FAQ, FAQCategory, SupportTicket, SupportReply, Notification, Feedback, ContactMessage
from . import email_service


# ─── FAQ ────────────────────────────────────────────────────────────────────

def faq_view(request):
    query = request.GET.get('q', '').strip()
    category_filter = request.GET.get('cat', '').strip()

    categories = FAQCategory.objects.prefetch_related('faqs').all()
    popular = FAQ.objects.filter(is_popular=True).select_related('category')[:6]

    faqs = FAQ.objects.select_related('category').all()
    if query:
        faqs = faqs.filter(Q(question__icontains=query) | Q(answer__icontains=query))
    if category_filter:
        faqs = faqs.filter(category__slug=category_filter)

    return render(request, 'core/faq.html', {
        'categories': categories,
        'popular': popular,
        'faqs': faqs,
        'query': query,
        'category_filter': category_filter,
    })


@require_POST
def faq_helpful(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)
    action = request.POST.get('action')
    if action == 'helpful':
        faq.helpful_count += 1
    else:
        faq.not_helpful_count += 1
    faq.save(update_fields=['helpful_count', 'not_helpful_count'])
    return JsonResponse({'helpful': faq.helpful_count, 'not_helpful': faq.not_helpful_count})


# ─── SUPPORT ────────────────────────────────────────────────────────────────

@login_required
def support_view(request):
    if request.method == 'POST':
        ticket = SupportTicket.objects.create(
            user=request.user,
            title=request.POST.get('title', '').strip(),
            issue_type=request.POST.get('issue_type', 'general'),
            priority=request.POST.get('priority', 'medium'),
            description=request.POST.get('description', '').strip(),
            screenshot=request.FILES.get('screenshot'),
        )
        email_service.send_ticket_created_email(ticket)
        messages.success(request, f'Ticket #{ticket.id} created successfully!')
        return redirect('core:support')

    tickets = SupportTicket.objects.filter(user=request.user).prefetch_related('replies')
    open_count = tickets.filter(status='open').count()
    pending_count = tickets.filter(status='pending').count()
    resolved_count = tickets.filter(status='resolved').count()

    return render(request, 'core/support.html', {
        'tickets': tickets,
        'open_count': open_count,
        'pending_count': pending_count,
        'resolved_count': resolved_count,
    })


@login_required
def ticket_detail_view(request, ticket_id):
    ticket = get_object_or_404(SupportTicket, id=ticket_id, user=request.user)
    if request.method == 'POST':
        msg = request.POST.get('message', '').strip()
        if msg:
            SupportReply.objects.create(ticket=ticket, user=request.user, message=msg)
            messages.success(request, 'Reply sent.')
        return redirect('core:ticket_detail', ticket_id=ticket.id)
    return render(request, 'core/ticket_detail.html', {'ticket': ticket})


# ─── NOTIFICATIONS ──────────────────────────────────────────────────────────

@login_required
def notifications_view(request):
    notifs = Notification.objects.filter(user=request.user)
    notifs.filter(is_read=False).update(is_read=True)
    return render(request, 'core/notifications.html', {'notifications': notifs})


@login_required
def notifications_api(request):
    unread = Notification.objects.filter(user=request.user, is_read=False)
    data = [{'id': n.id, 'title': n.title, 'message': n.message, 'type': n.notif_type,
              'link': n.link, 'time': n.created_at.strftime('%b %d, %H:%M')} for n in unread[:10]]
    return JsonResponse({'count': unread.count(), 'notifications': data})


@login_required
@require_POST
def mark_all_read(request):
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    return JsonResponse({'status': 'ok'})


@login_required
@require_POST
def delete_notification(request, notif_id):
    Notification.objects.filter(id=notif_id, user=request.user).delete()
    return JsonResponse({'status': 'ok'})


# ─── CONTACT ────────────────────────────────────────────────────────────────

def contact_view(request):
    if request.method == 'POST':
        ContactMessage.objects.create(
            name=request.POST.get('name', '').strip(),
            email=request.POST.get('email', '').strip(),
            subject=request.POST.get('subject', '').strip(),
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, 'Message sent! We\'ll get back to you within 24 hours.')
        return redirect('core:contact')
    return render(request, 'core/contact.html')


# ─── FEEDBACK ───────────────────────────────────────────────────────────────

def feedback_view(request):
    if request.method == 'POST':
        Feedback.objects.create(
            user=request.user if request.user.is_authenticated else None,
            name=request.POST.get('name', '').strip(),
            email=request.POST.get('email', '').strip(),
            category=request.POST.get('category', 'experience'),
            emotion=request.POST.get('emotion', 'happy'),
            rating=int(request.POST.get('rating', 5)),
            message=request.POST.get('message', '').strip(),
        )
        messages.success(request, 'Thank you for your feedback! 🙏')
        return redirect('core:feedback')

    recent = Feedback.objects.all()[:6]
    avg_rating = Feedback.objects.aggregate(avg=Avg('rating'))['avg'] or 0
    emotion_stats = Feedback.objects.values('emotion').annotate(count=Count('id'))

    return render(request, 'core/feedback.html', {
        'recent': recent,
        'avg_rating': round(avg_rating, 1),
        'emotion_stats': {e['emotion']: e['count'] for e in emotion_stats},
    })
