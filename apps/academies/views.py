from django.shortcuts import render
from django.db.models import Q
from .models import Academy

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
