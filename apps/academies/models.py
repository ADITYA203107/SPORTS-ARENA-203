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
