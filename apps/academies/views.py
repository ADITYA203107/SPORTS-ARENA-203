from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Academy, Booking

def explore_view(request):
    academies = Academy.objects.filter(is_active=True)
    
    # Get search and filter parameters
    search_query = request.GET.get('search', '')
    location_filter = request.GET.get('location', '')
    
    # Apply search filter
    if search_query:
        academies = academies.filter(
            Q(name__icontains=search_query) |
            Q(sport__icontains=search_query) |
            Q(coach_name__icontains=search_query)
        )
    
    # Apply location filter
    if location_filter:
        academies = academies.filter(city__icontains=location_filter)
    
    # Get unique cities for filter dropdown
    cities = Academy.objects.filter(is_active=True).values_list('city', flat=True).distinct()
    
    context = {
        'academies': academies,
        'search_query': search_query,
        'location_filter': location_filter,
        'cities': cities,
    }
    
    return render(request, 'academies/explore.html', context)

def home_view(request):
    # Get featured academies (latest 6)
    featured_academies = Academy.objects.filter(is_active=True)[:6]
    
    context = {
        'featured_academies': featured_academies,
    }
    
    return render(request, 'academies/home.html', context)

def detail_view(request, academy_id):
    academy = get_object_or_404(Academy, id=academy_id, is_active=True)
    
    context = {
        'academy': academy,
    }
    
    return render(request, 'academies/detail.html', context)

@login_required
def book_academy_view(request):
    if request.method == 'POST':
        academy_id = request.POST.get('academy_id')
        booking_date = request.POST.get('booking_date')
        notes = request.POST.get('notes', '')
        
        academy = get_object_or_404(Academy, id=academy_id)
        
        # Create the booking
        booking = Booking.objects.create(
            user=request.user,
            academy=academy,
            booking_date=booking_date,
            notes=notes,
            status='pending'
        )
        
        messages.success(request, f'Successfully booked {academy.name} for {booking_date}!')
        
        return redirect('accounts:dashboard')
    
    return redirect('academies:explore')
