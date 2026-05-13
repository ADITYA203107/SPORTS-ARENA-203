from django.urls import path

from . import views

app_name = 'academies'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('academy/<int:academy_id>/', views.detail_view, name='detail'),
    path('book/', views.book_academy_view, name='book_academy'),
    # Day 3 discovery & chat
    path('api/suggest/', views.api_search_suggestions, name='api_search_suggestions'),
    path('api/map-academies/', views.api_map_academies, name='api_map_academies'),
    path('api/favorite/<int:academy_id>/toggle/', views.api_toggle_favorite, name='api_toggle_favorite'),
    path('academy/<int:academy_id>/chat/', views.chat_open_or_create, name='chat_open'),
    path('messages/', views.chat_inbox_view, name='chat_inbox'),
    path('messages/<int:room_id>/', views.chat_room_view, name='chat_room'),
    path('api/messages/<int:room_id>/poll/', views.api_chat_poll, name='api_chat_poll'),
    path('api/messages/<int:room_id>/send/', views.api_chat_send, name='api_chat_send'),
    # API endpoints (require API key)
    path('api/academies/', views.api_academies_list, name='api_academies_list'),
    path('api/academies/<int:academy_id>/', views.api_academy_detail, name='api_academy_detail'),
    path('api/test/', views.api_test_auth, name='api_test'),
]
