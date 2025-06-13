from django.urls import path
from .views import redirect_to_dashboard, dashboard

urlpatterns = [
    path('', redirect_to_dashboard, name='home'),
    path('dashboard/', dashboard, name='dashboard'),
]