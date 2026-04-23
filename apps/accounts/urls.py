from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/manage-academy/', views.manage_academy_view, name='manage_academy'),
    path('dashboard/manage-coaches/', views.manage_coaches_view, name='manage_coaches'),
    path('dashboard/upload-photos/', views.upload_photos_view, name='upload_photos'),
    path('dashboard/view-bookings/', views.view_bookings_view, name='view_bookings'),
    path('dashboard/my-bookings/', views.my_bookings_view, name='my_bookings'),
    path('dashboard/booking/<int:booking_id>/<str:status>/', views.update_booking_status_view, name='update_booking_status'),
]
