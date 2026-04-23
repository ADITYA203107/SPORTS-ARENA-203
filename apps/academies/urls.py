from django.urls import path
from . import views

app_name = 'academies'

urlpatterns = [
    path('', views.home_view, name='home'),
    path('explore/', views.explore_view, name='explore'),
    path('academy/<int:academy_id>/', views.detail_view, name='detail'),
    path('book/', views.book_academy_view, name='book_academy'),
]
