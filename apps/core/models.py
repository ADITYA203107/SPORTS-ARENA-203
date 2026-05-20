from django.db import models
from django.conf import settings


# ─── FAQ ────────────────────────────────────────────────────────────────────

class FAQCategory(models.Model):
    CATEGORY_CHOICES = [
        ('learner', 'Learner'),
        ('owner', 'Academy Owner'),
        ('technical', 'Technical'),
    ]
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    category_type = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='learner')
    icon = models.CharField(max_length=50, default='❓')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class FAQ(models.Model):
    category = models.ForeignKey(FAQCategory, on_delete=models.CASCADE, related_name='faqs')
    question = models.CharField(max_length=300)
    answer = models.TextField()
    is_popular = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)
    not_helpful_count = models.PositiveIntegerField(default=0)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-helpful_count']

    def __str__(self):
        return self.question


# ─── SUPPORT TICKETS ────────────────────────────────────────────────────────

class SupportTicket(models.Model):
    ISSUE_CHOICES = [
        ('booking', 'Booking Issue'),
        ('chat', 'Chat Issue'),
        ('profile', 'Profile Issue'),
        ('academy', 'Academy Issue'),
        ('notification', 'Notification Issue'),
        ('general', 'General Support'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tickets')
    title = models.CharField(max_length=200)
    issue_type = models.CharField(max_length=20, choices=ISSUE_CHOICES, default='general')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='open')
    description = models.TextField()
    screenshot = models.ImageField(upload_to='support_screenshots/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'#{self.id} - {self.title}'


class SupportReply(models.Model):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name='replies')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    is_staff_reply = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Reply to #{self.ticket.id}'


# ─── NOTIFICATIONS ──────────────────────────────────────────────────────────

class Notification(models.Model):
    TYPE_CHOICES = [
        ('booking_approved', 'Booking Approved'),
        ('booking_rejected', 'Booking Rejected'),
        ('new_booking', 'New Booking'),
        ('new_message', 'New Message'),
        ('academy_reply', 'Academy Reply'),
        ('ticket_reply', 'Support Reply'),
        ('ticket_created', 'Ticket Created'),
        ('system', 'System'),
        ('welcome', 'Welcome'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notif_type = models.CharField(max_length=30, choices=TYPE_CHOICES, default='system')
    is_read = models.BooleanField(default=False)
    link = models.CharField(max_length=300, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.user.username} — {self.title}'


# ─── FEEDBACK ───────────────────────────────────────────────────────────────

class Feedback(models.Model):
    EMOTION_CHOICES = [
        ('happy', '😀 Happy'),
        ('neutral', '😐 Neutral'),
        ('sad', '😞 Sad'),
    ]
    CATEGORY_CHOICES = [
        ('suggestion', 'Suggestion'),
        ('experience', 'Experience'),
        ('problem', 'Problem'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    name = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='experience')
    emotion = models.CharField(max_length=10, choices=EMOTION_CHOICES, default='happy')
    rating = models.PositiveSmallIntegerField(default=5)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.emotion} — {self.category} by {self.name or "Anonymous"}'


# ─── EMAIL LOG ──────────────────────────────────────────────────────────────

class EmailLog(models.Model):
    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('failed', 'Failed'),
        ('pending', 'Pending'),
    ]

    recipient = models.EmailField()
    subject = models.CharField(max_length=300)
    event_type = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.event_type} → {self.recipient} [{self.status}]'


# ─── CONTACT MESSAGE ────────────────────────────────────────────────────────

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} — {self.subject}'
