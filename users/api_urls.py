from django.urls import path
from .views import RegisterAPIView, CustomTokenObtainPairView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='api-register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
]