import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q, Count
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_GET, require_POST

from .api_auth import APIKeyAuthentication, require_api_key
from .chat_access import user_can_access_chat_room
from .models import Academy, Booking, ChatRoom, FavoriteAcademy, Message
from . import services


def explore_view(request):
    academies = Academy.objects.filter(is_active=True)

    search_query = request.GET.get('search', '').strip()
    location_filter = request.GET.get('location', '').strip()
    sport_filter = request.GET.get('sport', '').strip()
    try:
        radius_km = float(request.GET.get('radius', '') or 0)
    except ValueError:
        radius_km = 0.0
    try:
        user_lat = float(request.GET.get('lat', '') or 0)
        user_lng = float(request.GET.get('lng', '') or 0)
    except ValueError:
        user_lat = user_lng = 0.0

    if search_query:
        academies = academies.filter(
            Q(name__icontains=search_query)
            | Q(sport__icontains=search_query)
            | Q(coach_name__icontains=search_query)
            | Q(city__icontains=search_query)
        )
        services.log_activity(
            request,
            'search',
            query=search_query,
            sport=sport_filter,
            city=location_filter,
        )

    if location_filter:
        academies = academies.filter(city__icontains=location_filter)

    if sport_filter:
        academies = academies.filter(sport=sport_filter)

    academies_list = list(academies)
    distances = {}
    if radius_km > 0 and user_lat and user_lng:
        kept = []
        for a in academies_list:
            plat, plng = services.approximate_coords(a)
            d = services.haversine_km(user_lat, user_lng, plat, plng)
            distances[a.id] = round(d, 1)
            if d <= radius_km:
                kept.append(a)
        academies_list = kept

    cities = Academy.objects.filter(is_active=True).values_list('city', flat=True).distinct()

    map_markers = []
    for a in Academy.objects.filter(is_active=True):
        plat, plng = services.approximate_coords(a)
        d_km = None
        if user_lat and user_lng:
            d_km = round(services.haversine_km(user_lat, user_lng, plat, plng), 1)
        map_markers.append(
            {
                'id': a.id,
                'name': a.name,
                'sport': a.get_sport_display(),
                'city': a.city,
                'lat': plat,
                'lng': plng,
                'fees': float(a.fees),
                'rating': float(a.rating),
                'url': f'/academy/{a.id}/',
                'distance_km': d_km,
            }
        )

    compare_json = [
        {
            'id': a.id,
            'name': a.name,
            'sport': a.get_sport_display(),
            'city': a.city,
            'fees': float(a.fees),
            'rating': float(a.rating),
            'coaches': a.total_coaches,
            'coach_name': a.coach_name,
            'coach_years': a.coach_experience,
            'facilities': a.facilities_list[:6],
            'hours': a.opening_hours or '—',
            'distance_km': distances.get(a.id),
            'url': f'/academy/{a.id}/',
        }
        for a in academies_list
    ]

    all_compare = []
    for a in Academy.objects.filter(is_active=True)[:150]:
        plat, plng = services.approximate_coords(a)
        d_km = None
        if user_lat and user_lng:
            d_km = round(services.haversine_km(user_lat, user_lng, plat, plng), 1)
        all_compare.append(
            {
                'id': a.id,
                'name': a.name,
                'sport': a.get_sport_display(),
                'city': a.city,
                'fees': float(a.fees),
                'rating': float(a.rating),
                'coaches': a.total_coaches,
                'coach_name': a.coach_name,
                'coach_years': a.coach_experience,
                'facilities': a.facilities_list[:6],
                'hours': a.opening_hours or '—',
                'distance_km': d_km,
                'url': f'/academy/{a.id}/',
            }
        )

    trending_sports = services.trending_sports()
    trending_searches = services.trending_searches()
    recs, rec_ctx = services.recommended_academies(request, limit=4)

    context = {
        'academies': academies_list,
        'search_query': search_query,
        'location_filter': location_filter,
        'sport_filter': sport_filter,
        'cities': cities,
        'map_markers_json': json.dumps(map_markers),
        'compare_pool_json': json.dumps(compare_json),
        'all_compare_json': json.dumps(all_compare),
        'trending_sports': trending_sports,
        'trending_searches': trending_searches,
        'smart_recommendations': recs,
        'recommendation_blurb': rec_ctx,
        'user_lat': user_lat,
        'user_lng': user_lng,
        'radius_km': radius_km,
        'favorite_ids': services.user_favorite_ids(request),
    }

    return render(request, 'academies/explore.html', context)


def home_view(request):
    featured_academies = Academy.objects.filter(is_active=True)[:6]
    recent = services.recent_academy_views(request, limit=8)
    recs, rec_ctx = services.recommended_academies(request, limit=6)
    trending_sports = services.trending_sports()
    trending_searches = services.trending_searches()

    context = {
        'featured_academies': featured_academies,
        'recently_viewed': recent,
        'smart_recommendations': recs,
        'recommendation_blurb': rec_ctx,
        'trending_sports': trending_sports,
        'trending_searches': trending_searches,
    }

    return render(request, 'academies/home.html', context)


def detail_view(request, academy_id):
    academy = get_object_or_404(Academy, id=academy_id, is_active=True)
    services.log_activity(
        request,
        'view_academy',
        sport=academy.sport,
        city=academy.city,
        academy=academy,
    )

    plat, plng = services.approximate_coords(academy)
    nearby = []
    for a in Academy.objects.filter(is_active=True).exclude(id=academy.id)[:40]:
        alat, alng = services.approximate_coords(a)
        d = services.haversine_km(plat, plng, alat, alng)
        nearby.append((d, a))
    nearby.sort(key=lambda x: x[0])
    nearby = [{'academy': a, 'distance_km': round(d, 1)} for d, a in nearby[:5]]

    rec_same_sport = (
        Academy.objects.filter(is_active=True, sport=academy.sport)
        .exclude(id=academy.id)
        .order_by('-rating', 'fees')[:4]
    )

    is_favorite = False
    if request.user.is_authenticated:
        is_favorite = FavoriteAcademy.objects.filter(user=request.user, academy=academy).exists()

    can_chat = request.user.is_authenticated and (
        not academy.owner_id or request.user.id != academy.owner_id
    )

    context = {
        'academy': academy,
        'map_lat': plat,
        'map_lng': plng,
        'nearby': nearby,
        'rec_same_sport': rec_same_sport,
        'is_favorite': is_favorite,
        'can_chat': can_chat,
    }

    return render(request, 'academies/detail.html', context)


@login_required
def book_academy_view(request):
    if request.method == 'POST':
        academy_id = request.POST.get('academy_id', '').strip()
        booking_date = request.POST.get('booking_date')
        notes = request.POST.get('notes', '')

        if not academy_id or not academy_id.isdigit():
            messages.error(request, 'Invalid academy. Please try booking again.')
            return redirect('academies:explore')

        academy = get_object_or_404(Academy, id=academy_id)

        Booking.objects.create(
            user=request.user,
            academy=academy,
            booking_date=booking_date,
            notes=notes,
            status='pending',
        )
        services.log_activity(
            request,
            'booking',
            sport=academy.sport,
            city=academy.city,
            academy=academy,
            extra={'date': str(booking_date)},
        )

        messages.success(request, f'Successfully booked {academy.name} for {booking_date}!')

        return redirect('accounts:dashboard')

    return redirect('academies:explore')


# ==================== Discovery JSON (session auth) ====================


@require_GET
def api_search_suggestions(request):
    q = request.GET.get('q', '')
    return JsonResponse(services.search_suggestions_payload(q))


@require_GET
def api_map_academies(request):
    """Markers for map layer (respects optional sport/city query)."""
    qs = Academy.objects.filter(is_active=True)
    sport = request.GET.get('sport', '').strip()
    city = request.GET.get('city', '').strip()
    if sport:
        qs = qs.filter(sport=sport)
    if city:
        qs = qs.filter(city__icontains=city)
    try:
        user_lat = float(request.GET.get('lat', '') or 0)
        user_lng = float(request.GET.get('lng', '') or 0)
    except ValueError:
        user_lat = user_lng = 0.0
    try:
        radius_km = float(request.GET.get('radius', '') or 0)
    except ValueError:
        radius_km = 0.0

    markers = []
    for a in qs[:200]:
        plat, plng = services.approximate_coords(a)
        d_km = None
        if user_lat and user_lng:
            d_km = round(services.haversine_km(user_lat, user_lng, plat, plng), 1)
        if radius_km > 0 and user_lat and user_lng:
            if d_km is None or d_km > radius_km:
                continue
        markers.append(
            {
                'id': a.id,
                'name': a.name,
                'sport': a.get_sport_display(),
                'city': a.city,
                'lat': plat,
                'lng': plng,
                'fees': float(a.fees),
                'rating': float(a.rating),
                'url': f'/academy/{a.id}/',
                'distance_km': d_km,
            }
        )
    return JsonResponse({'markers': markers})


@login_required
@require_POST
def api_toggle_favorite(request, academy_id):
    academy = get_object_or_404(Academy, id=academy_id, is_active=True)
    fav, created = FavoriteAcademy.objects.get_or_create(user=request.user, academy=academy)
    if not created:
        fav.delete()
        services.log_activity(request, 'favorite_remove', academy=academy, sport=academy.sport)
        return JsonResponse({'favorited': False})
    services.log_activity(request, 'favorite_add', academy=academy, sport=academy.sport)
    return JsonResponse({'favorited': True})


@login_required
def chat_open_or_create(request, academy_id):
    academy = get_object_or_404(Academy, id=academy_id, is_active=True)
    if academy.owner_id and request.user.id == academy.owner_id:
        messages.info(request, 'Use your inbox to reply to learners.')
        return redirect('academies:chat_inbox')
    room, _ = ChatRoom.objects.get_or_create(academy=academy, learner=request.user)
    return redirect('academies:chat_room', room_id=room.id)


@login_required
def chat_inbox_view(request):
    if request.user.role == 'academy':
        rooms = ChatRoom.objects.filter(academy__owner=request.user).select_related('academy', 'learner')
    else:
        rooms = ChatRoom.objects.filter(learner=request.user).select_related('academy', 'learner')
    rooms = rooms.annotate(msg_count=Count('messages')).order_by('-updated_at')
    return render(request, 'academies/chat_inbox.html', {'rooms': rooms})


@login_required
def chat_room_view(request, room_id):
    room = get_object_or_404(ChatRoom.objects.select_related('academy', 'academy__owner', 'learner'), id=room_id)
    if not user_can_access_chat_room(request, room):
        messages.error(request, 'You do not have access to this conversation.')
        return redirect('academies:explore')
    room.academy.refresh_from_db()
    msgs = list(room.messages.select_related('sender').order_by('created_at')[:500])
    Message.objects.filter(room=room, read_at__isnull=True).exclude(sender=request.user).update(
        read_at=timezone.now()
    )
    if request.user.id == room.learner_id:
        peer = room.academy.owner
        peer_label = room.academy.owner.username if room.academy.owner_id else 'Academy team'
    else:
        peer = room.learner
        peer_label = room.learner.username
    last_message_id = msgs[-1].id if msgs else 0
    return render(
        request,
        'academies/chat_room.html',
        {
            'room': room,
            'messages_list': msgs,
            'peer': peer,
            'peer_label': peer_label,
            'academy': room.academy,
            'last_message_id': last_message_id,
        },
    )


@login_required
@require_GET
def api_chat_poll(request, room_id):
    room = get_object_or_404(ChatRoom.objects.select_related('academy'), id=room_id)
    if not user_can_access_chat_room(request, room):
        return JsonResponse({'error': 'forbidden'}, status=403)
    try:
        after_id = int(request.GET.get('after', '0'))
    except ValueError:
        after_id = 0
    qs = room.messages.filter(id__gt=after_id).select_related('sender').order_by('created_at')
    out = []
    for m in qs[:100]:
        out.append(
            {
                'id': m.id,
                'body': m.body,
                'sender_id': m.sender_id,
                'is_mine': m.sender_id == request.user.id,
                'created_at': m.created_at.isoformat(),
            }
        )
    return JsonResponse({'messages': out})


@login_required
@require_POST
def api_chat_send(request, room_id):
    room = get_object_or_404(ChatRoom.objects.select_related('academy'), id=room_id)
    if not user_can_access_chat_room(request, room):
        return JsonResponse({'error': 'forbidden'}, status=403)
    try:
        payload = json.loads(request.body.decode() or '{}')
    except json.JSONDecodeError:
        payload = {}
    body = (payload.get('body') or '').strip()
    if not body:
        return JsonResponse({'error': 'empty'}, status=400)
    msg = Message.objects.create(room=room, sender=request.user, body=body[:4000])
    ChatRoom.objects.filter(pk=room.pk).update(updated_at=timezone.now())
    return JsonResponse(
        {
            'id': msg.id,
            'body': msg.body,
            'sender_id': msg.sender_id,
            'is_mine': True,
            'created_at': msg.created_at.isoformat(),
        }
    )


# ==================== API ENDPOINTS WITH API KEY AUTH ====================


@require_api_key
def api_academies_list(request):
    academies = Academy.objects.filter(is_active=True)

    data = []
    for academy in academies:
        data.append(
            {
                'id': academy.id,
                'name': academy.name,
                'sport': academy.get_sport_display(),
                'location': academy.location,
                'city': academy.city,
                'fees': float(academy.fees),
                'coach_name': academy.coach_name,
                'coach_experience': academy.coach_experience,
            }
        )

    return JsonResponse({'status': 'success', 'count': len(data), 'data': data})


@require_api_key
def api_academy_detail(request, academy_id):
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

        return JsonResponse({'status': 'success', 'data': data})

    except Academy.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Academy not found'}, status=404)


def api_test_auth(request):
    auth = APIKeyAuthentication.authenticate(request)
    key_obj, error = auth

    if error:
        return JsonResponse({'status': 'error', 'message': error['error']}, status=error['code'])

    return JsonResponse(
        {
            'status': 'success',
            'message': 'API key is valid',
            'api_key_name': key_obj.name,
            'created_at': key_obj.created_at.isoformat(),
            'last_used_at': key_obj.last_used_at.isoformat() if key_obj.last_used_at else None,
        }
    )
