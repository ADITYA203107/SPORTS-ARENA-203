from django.urls import path
from . import views

app_name = 'academies'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('academy/<int:academy_id>/', views.detail_view, name='detail'),
    path('book/', views.book_academy_view, name='book_academy'),
    
    # API endpoints (require API key)
    path('api/academies/', views.api_academies_list, name='api_academies_list'),
    path('api/academies/<int:academy_id>/', views.api_academy_detail, name='api_academy_detail'),
    path('api/test/', views.api_test_auth, name='api_test'),
]
