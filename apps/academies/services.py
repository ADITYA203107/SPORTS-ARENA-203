"""Discovery, activity, and recommendation helpers (Day 3)."""
from __future__ import annotations

import math
from collections import Counter
from datetime import timedelta

from django.db.models import Count, Q
from django.utils import timezone

from .models import Academy, UserActivity, FavoriteAcademy, Coach


def session_key_for(request) -> str:
    if not request.session.session_key:
        request.session.create()
    return request.session.session_key or ''


def log_activity(
    request,
    activity: str,
    *,
    query: str = '',
    sport: str = '',
    city: str = '',
    academy=None,
    extra=None,
):
    UserActivity.objects.create(
        user=request.user if request.user.is_authenticated else None,
        session_key=session_key_for(request),
        activity=activity,
        query=(query or '')[:255],
        sport=(sport or '')[:32],
        city=(city or '')[:120],
        academy=academy,
        extra=extra or {},
    )


def approximate_coords(academy: Academy) -> tuple[float, float]:
    """Fallback map position when lat/lng not set (India-centric grid)."""
    if academy.latitude is not None and academy.longitude is not None:
        return float(academy.latitude), float(academy.longitude)
    seed = academy.id or 1
    lat = 12.97 + (seed % 17) * 0.35
    lng = 77.59 + (seed % 23) * 0.28
    return lat, lng


def haversine_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    r = 6371.0
    p1, p2 = math.radians(lat1), math.radians(lat2)
    dp = math.radians(lat2 - lat1)
    dl = math.radians(lon2 - lon1)
    a = math.sin(dp / 2) ** 2 + math.cos(p1) * math.cos(p2) * math.sin(dl / 2) ** 2
    return 2 * r * math.asin(math.sqrt(min(1.0, a)))


def trending_searches(days: int = 7, limit: int = 8):
    since = timezone.now() - timedelta(days=days)
    rows = (
        UserActivity.objects.filter(activity='search', created_at__gte=since)
        .exclude(query='')
        .values_list('query', flat=True)
    )
    counts = Counter(q.strip().lower() for q in rows if q and len(q.strip()) > 1)
    return [q for q, _ in counts.most_common(limit)]


def trending_sports(days: int = 7, limit: int = 6):
    since = timezone.now() - timedelta(days=days)
    sport_qs = (
        UserActivity.objects.filter(created_at__gte=since)
        .exclude(sport='')
        .values('sport')
        .annotate(c=Count('id'))
        .order_by('-c')[:limit]
    )
    out = [row['sport'] for row in sport_qs]
    if len(out) < limit:
        popular = (
            Academy.objects.filter(is_active=True)
            .values('sport')
            .annotate(c=Count('id'))
            .order_by('-c')
        )
        for row in popular:
            if row['sport'] not in out:
                out.append(row['sport'])
            if len(out) >= limit:
                break
    return out[:limit]


def recent_academy_views(request, limit: int = 12):
    sk = session_key_for(request)
    q = Q(session_key=sk)
    if request.user.is_authenticated:
        q |= Q(user=request.user)
    ids = list(
        UserActivity.objects.filter(q, activity='view_academy', academy__isnull=False)
        .order_by('-created_at')
        .values_list('academy_id', flat=True)[: limit * 3]
    )
    seen = set()
    ordered_ids = []
    for pk in ids:
        if pk not in seen:
            seen.add(pk)
            ordered_ids.append(pk)
        if len(ordered_ids) >= limit:
            break
    if not ordered_ids:
        return Academy.objects.none()
    preserved = {pk: i for i, pk in enumerate(ordered_ids)}
    qs = Academy.objects.filter(id__in=ordered_ids, is_active=True)
    return sorted(qs, key=lambda a: preserved.get(a.id, 999))


def recommendation_context(request):
    """Sports / queries to drive 'Because you…' strip."""
    sk = session_key_for(request)
    q = Q(session_key=sk)
    if request.user.is_authenticated:
        q |= Q(user=request.user)
    last_search = (
        UserActivity.objects.filter(q, activity='search')
        .exclude(query='')
        .order_by('-created_at')
        .values_list('query', flat=True)
        .first()
    )
    last_sport = (
        UserActivity.objects.filter(q)
        .exclude(sport='')
        .order_by('-created_at')
        .values_list('sport', flat=True)
        .first()
    )
    if not last_sport and last_search:
        term = last_search.lower()
        for val, label in Academy.SPORT_CHOICES:
            if val in term or label.lower() in term:
                last_sport = val
                break
    return {'last_search': last_search or '', 'last_sport': last_sport or ''}


def recommended_academies(request, limit: int = 6):
    ctx = recommendation_context(request)
    sport = ctx['last_sport']
    qs = Academy.objects.filter(is_active=True)
    if sport:
        qs = qs.filter(sport=sport)
    popular = (
        Academy.objects.filter(is_active=True)
        .annotate(vc=Count('activities', filter=Q(activities__activity='view_academy')))
        .order_by('-vc', '-rating', 'fees')[: limit * 2]
    )
    merged = list(qs[:limit])
    if len(merged) < limit:
        for a in popular:
            if a not in merged:
                merged.append(a)
            if len(merged) >= limit:
                break
    return merged[:limit], ctx


def search_suggestions_payload(q: str, limit: int = 10) -> dict:
    q = (q or '').strip()
    if len(q) < 2:
        return {'query': q, 'suggestions': [], 'trending': trending_searches()}
    ql = q.lower()
    suggestions = []

    for val, label in Academy.SPORT_CHOICES:
        if ql in label.lower() or ql in val:
            suggestions.append(
                {
                    'type': 'sport',
                    'icon': '🏅',
                    'title': f'{label} academies',
                    'subtitle': 'Live programs & trials',
                    'url': f'/explore/?sport={val}',
                }
            )
            suggestions.append(
                {
                    'type': 'coach',
                    'icon': '🎯',
                    'title': f'{label} coaches',
                    'subtitle': 'Specialist coaching talent',
                    'url': f'/explore/?search={label}+coach',
                }
            )

    cities = (
        Academy.objects.filter(is_active=True, city__icontains=q)
        .values_list('city', flat=True)
        .distinct()[:5]
    )
    for city in cities:
        suggestions.append(
            {
                'type': 'city',
                'icon': '📍',
                'title': f'{q.title()} in {city}',
                'subtitle': 'Hyperlocal discovery',
                'url': f'/explore/?location={city}&search={q}',
            }
        )

    for a in Academy.objects.filter(is_active=True).filter(
        Q(name__icontains=q) | Q(coach_name__icontains=q) | Q(location__icontains=q)
    )[:5]:
        suggestions.append(
            {
                'type': 'academy',
                'icon': '🏟️',
                'title': a.name,
                'subtitle': f'{a.get_sport_display()} · {a.city}',
                'url': f'/academy/{a.id}/',
            }
        )

    seen = set()
    deduped = []
    for s in suggestions:
        key = (s['type'], s['title'], s['url'])
        if key in seen:
            continue
        seen.add(key)
        deduped.append(s)
        if len(deduped) >= limit:
            break

    coach_hits = Coach.objects.filter(Q(name__icontains=q) | Q(sport__icontains=q))[:3]
    for c in coach_hits:
        deduped.append(
            {
                'type': 'coach_profile',
                'icon': '⚡',
                'title': f'{c.name} ({c.get_sport_display()})',
                'subtitle': f'{c.experience}+ yrs experience',
                'url': f'/explore/?search={c.name}',
            }
        )

    return {'query': q, 'suggestions': deduped[:limit], 'trending': trending_searches()}


def user_favorite_ids(request) -> set[int]:
    if not request.user.is_authenticated:
        return set()
    return set(FavoriteAcademy.objects.filter(user=request.user).values_list('academy_id', flat=True))
