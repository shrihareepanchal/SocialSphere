from django.urls import path
from . import views

app_name = 'search'

urlpatterns = [
    path('', views.search_view, name='search'),
    path('api/', views.search_api, name='search_api'),
    path('suggestions/', views.search_suggestions, name='search_suggestions'),
]
