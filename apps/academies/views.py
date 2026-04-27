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


# ==================== API ENDPOINTS WITH API KEY AUTH ====================

from django.http import JsonResponse
from .api_auth import require_api_key, APIKeyAuthentication
from .models import APIKey
import json


@require_api_key
def api_academies_list(request):
    """
    API endpoint to list all academies.
    Requires X-API-Key header.
    
    GET /api/academies/
    Header: X-API-Key: your-api-key
    """
    academies = Academy.objects.filter(is_active=True)
    
    data = []
    for academy in academies:
        data.append({
            'id': academy.id,
            'name': academy.name,
            'sport': academy.get_sport_display(),
            'location': academy.location,
            'city': academy.city,
            'fees': float(academy.fees),
            'coach_name': academy.coach_name,
            'coach_experience': academy.coach_experience,
        })
    
    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'data': data
    })


@require_api_key
def api_academy_detail(request, academy_id):
    """
    API endpoint to get academy details.
    Requires X-API-Key header.
    
    GET /api/academies/<id>/
    Header: X-API-Key: your-api-key
    """
    try:
        academy = Academy.objects.get(id=academy_id, is_active=True)
        
        data = {
            'id': academy.id,
            'name': academy.name,
            'sport': academy.get_sport_display(),
            'location': academy.location,
            'city': academy.city,
            'fees': float(academy.fees),
            'coach_name': academy.coach_name,
            'coach_experience': academy.coach_experience,
            'description': academy.description,
            'image_url': academy.image.url if academy.image else None,
            'phone': academy.phone,
            'email': academy.email,
            'website': academy.website,
        }
        
        return JsonResponse({
            'status': 'success',
            'data': data
        })
    
    except Academy.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Academy not found'
        }, status=404)


def api_test_auth(request):
    """
    Test API key authentication.
    Requires X-API-Key header.
    
    GET /api/test/
    Header: X-API-Key: your-api-key
    """
    auth = APIKeyAuthentication.authenticate(request)
    key_obj, error = auth
    
    if error:
        return JsonResponse({
            'status': 'error',
            'message': error['error']
        }, status=error['code'])
    
    return JsonResponse({
        'status': 'success',
        'message': 'API key is valid',
        'api_key_name': key_obj.name,
        'created_at': key_obj.created_at.isoformat(),
        'last_used_at': key_obj.last_used_at.isoformat() if key_obj.last_used_at else None
    })
