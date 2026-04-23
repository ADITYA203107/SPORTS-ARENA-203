from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from apps.academies.models import Academy, Coach
from apps.academies.forms import CoachForm, AcademyForm
from apps.academies.models import Booking

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
    
    academies = Academy.objects.all()
    
    if request.user.role == 'academy':
        coaches = Coach.objects.all()
        return render(request, 'accounts/dashboard.html', {'academies': academies})
    else:
        # Player dashboard
        return render(request, 'accounts/player_dashboard.html', {'academies': academies})

def logout_view(request):
    if request.method == 'POST':
        logout(request)
        messages.success(request, 'You have been logged out successfully.')
    return redirect('academies:home')

def profile_view(request):
    if not request.user.is_authenticated:
        return redirect('accounts:login')
    
    return render(request, 'accounts/profile.html')

@login_required
def manage_academy_view(request):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    if request.method == 'POST':
        form = AcademyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Academy added successfully!')
            return redirect('accounts:manage_academy')
    else:
        form = AcademyForm()
    
    academies = Academy.objects.all()
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
    
    academies = Academy.objects.all()
    coaches = Coach.objects.all()
    return render(request, 'accounts/manage_coaches.html', {'academies': academies, 'coaches': coaches, 'form': form})

@login_required
def upload_photos_view(request):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    academies = Academy.objects.all()
    return render(request, 'accounts/upload_photos.html', {'academies': academies})

@login_required
def view_bookings_view(request):
    if request.user.role != 'academy':
        messages.error(request, 'Access denied. Academy owners only.')
        return redirect('academies:explore')
    
    academies = Academy.objects.all()
    bookings = Booking.objects.all()
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
    
    booking = get_object_or_404(Booking, id=booking_id)
    booking.status = status
    booking.save()
    
    messages.success(request, f'Booking {status} successfully!')
    return redirect('accounts:view_bookings')
