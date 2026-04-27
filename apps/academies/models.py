from django.db import models
from django.conf import settings

class Coach(models.Model):
    SPORT_CHOICES = [
        ('badminton', 'Badminton'),
        ('swimming', 'Swimming'),
        ('tennis', 'Tennis'),
        ('football', 'Football'),
        ('cricket', 'Cricket'),
        ('basketball', 'Basketball'),
        ('volleyball', 'Volleyball'),
        ('table_tennis', 'Table Tennis'),
        ('chess', 'Chess'),
        ('yoga', 'Yoga'),
    ]
    
    name = models.CharField(max_length=200)
    sport = models.CharField(max_length=20, choices=SPORT_CHOICES)
    experience = models.IntegerField(help_text="Years of experience")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_sport_display()} ({self.experience} years)"

class Academy(models.Model):
    SPORT_CHOICES = [
        ('badminton', 'Badminton'),
        ('swimming', 'Swimming'),
        ('tennis', 'Tennis'),
        ('football', 'Football'),
        ('cricket', 'Cricket'),
        ('basketball', 'Basketball'),
        ('volleyball', 'Volleyball'),
        ('table_tennis', 'Table Tennis'),
        ('chess', 'Chess'),
        ('yoga', 'Yoga'),
    ]
    
    name = models.CharField(max_length=200)
    sport = models.CharField(max_length=20, choices=SPORT_CHOICES)
    location = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    fees = models.DecimalField(max_digits=10, decimal_places=2)
    coach_name = models.CharField(max_length=100)
    coach_experience = models.IntegerField(help_text="Years of experience")
    description = models.TextField()
    image = models.ImageField(upload_to='academy_images/', blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    website = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.name} - {self.get_sport_display()}"
    
    @property
    def coach_info(self):
        return f"{self.coach_name} ({self.coach_experience} years)"

class Booking(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('rejected', 'Rejected'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='bookings')
    academy = models.ForeignKey(Academy, on_delete=models.CASCADE, related_name='bookings')
    booking_date = models.DateField()
    notes = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.academy.name} ({self.booking_date})"


import secrets
import hashlib

class APIKey(models.Model):
    key = models.CharField(max_length=64, unique=True, editable=False)
    name = models.CharField(max_length=100, help_text="Name for this API key (e.g., 'Mobile App', 'Partner Integration')")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='api_keys', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_used_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'API Key'
        verbose_name_plural = 'API Keys'
    
    def save(self, *args, **kwargs):
        if not self.key:
            # Generate a new API key
            raw_key = secrets.token_urlsafe(32)
            # Store hashed version for security (optional - can store raw if needed)
            self.key = hashlib.sha256(raw_key.encode()).hexdigest()[:64]
            # Store the raw key temporarily to display to user (only once)
            self._raw_key = raw_key
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.name} ({'Active' if self.is_active else 'Inactive'})"
    
    @classmethod
    def generate_raw_key(cls):
        """Generate a new raw API key"""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def hash_key(cls, raw_key):
        """Hash a raw API key"""
        return hashlib.sha256(raw_key.encode()).hexdigest()[:64]
    
    @classmethod
    def validate_key(cls, raw_key):
        """Validate an API key and return the key object if valid"""
        hashed = cls.hash_key(raw_key)
        try:
            api_key = cls.objects.get(key=hashed, is_active=True)
            return api_key
        except cls.DoesNotExist:
            return None
