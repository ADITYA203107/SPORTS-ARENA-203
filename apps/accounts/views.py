from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from apps.academies.models import Academy, Booking, ChatRoom, Coach, FavoriteAcademy
from apps.academies.forms import CoachForm, AcademyForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Account created successfully! Please log in.')
            return redirect('accounts:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'accounts/signup.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                
                # Role-based redirection
                if user.role == 'learner':
                    return redirect('academies:explore')
                elif user.role == 'academy':
                    return redirect('accounts:dashboard')
                else:
                    return redirect('academies:explore')
            else:
                messages.error(request, 'Invalid email or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})

def dashboard_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    if request.user.role == 'academy':
        my_academies = Academy.objects.filter(owner=request.user)
        coach_count = Coach.objects.count()
        booking_count = Booking.objects.filter(academy__owner=request.user).count()
        chat_count = ChatRoom.objects.filter(academy__owner=request.user).count()
        recent_bookings = (
            Booking.objects.filter(academy__owner=request.user)
            .select_related('user', 'academy')
            .order_by('-created_at')[:10]
        )
        return render(
            request,
            'accounts/dashboard.html',
            {
                'my_academies': my_academies,
                'academy_count': my_academies.count(),
                'coach_count': coach_count,
                'booking_count': booking_count,
                'chat_count': chat_count,
                'recent_bookings': recent_bookings,
            },
        )

    academies = Academy.objects.filter(is_active=True)[:12]
    return render(request, 'accounts/player_dashboard.html', {'academies': academies})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('academies:home')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')

    user = request.user
    bookings = (
        Booking.objects.filter(user=user)
        .select_related('academy')
        .order_by('-created_at')[:50]
    )
    favorite_entries = (
        FavoriteAcademy.objects.filter(user=user)
        .select_related('academy')
        .order_by('-created_at')[:30]
    )

    if user.role == 'academy':
        chat_rooms = (
            ChatRoom.objects.filter(academy__owner=user)
            .select_related('academy', 'learner')
            .order_by('-updated_at')[:30]
        )
        academies_for_chat = []
    else:
        chat_rooms = (
            ChatRoom.objects.filter(learner=user)
            .select_related('academy', 'academy__owner')
            .order_by('-updated_at')[:30]
        )
        academies_for_chat = list(
            Academy.objects.filter(is_active=True)
            .exclude(owner=user)
            .order_by('-rating', 'name')[:24]
        )

    return render(
        request,
        'accounts/profile.html',
        {
            'bookings': bookings,
            'favorite_entries': favorite_entries,
            'chat_rooms': chat_rooms,
            'academies_for_chat': academies_for_chat,
        },
    )

@login_required
def manage_academy_view(request):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    if request.method == 'POST':
        form = AcademyForm(request.POST, request.FILES)
        if form.is_valid():
            academy = form.save(commit=False)
            academy.owner = request.user
            academy.save()
            messages.success(request, 'Academy added successfully!')
            return redirect('accounts:manage_academy')
    else:
        form = AcademyForm()
    
    academies = Academy.objects.filter(owner=request.user)
    coaches = Coach.objects.all()
    return render(request, 'accounts/manage_academy.html', {'academies': academies, 'coaches': coaches, 'form': form})

@login_required
def manage_coaches_view(request):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    if request.method == 'POST':
        form = CoachForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Coach added successfully!')
            return redirect('accounts:manage_coaches')
    else:
        form = CoachForm()
    
    academies = Academy.objects.filter(owner=request.user)
    coaches = Coach.objects.all()
    return render(request, 'accounts/manage_coaches.html', {'academies': academies, 'coaches': coaches, 'form': form})

@login_required
def upload_photos_view(request):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    academies = Academy.objects.filter(owner=request.user)
    return render(request, 'accounts/upload_photos.html', {'academies': academies})

@login_required
def view_bookings_view(request):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    academies = Academy.objects.filter(owner=request.user)
    bookings = (
        Booking.objects.filter(academy__owner=request.user)
        .select_related('user', 'academy')
        .order_by('-created_at')
    )
    return render(request, 'accounts/view_bookings.html', {'academies': academies, 'bookings': bookings})

@login_required
def my_bookings_view(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'accounts/my_bookings.html', {'bookings': bookings})

@login_required
def update_booking_status_view(request, booking_id, status):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    booking = get_object_or_404(Booking, id=booking_id, academy__owner=request.user)
    booking.status = status
    booking.save()
    
    messages.success(request, f'Booking {status} successfully!')
    return redirect('accounts:view_bookings')
