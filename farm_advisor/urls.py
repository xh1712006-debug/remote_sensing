from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('api/analyze/', views.api_analyze_farm, name='api_analyze'),
]
