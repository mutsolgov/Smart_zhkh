from django.urls import path
from . import html_views

urlpatterns = [
    path('', html_views.ChargePeriodSelectView.as_view(), name='charge-period-select'),
    path('list/', html_views.ChargeListView.as_view(), name='charge-list'),
    path('<int:pk>/', html_views.ChargeDetailView.as_view(), name='charge-detail'),
]