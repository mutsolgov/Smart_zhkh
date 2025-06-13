from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from users import views as user_views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include('users.api_urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/charges/', include('charges.urls')),
    path('api/payments/', include('payments.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('openid/', include('oidc_provider.urls', namespace='oidc_provider')),

    path('register/', user_views.RegisterHTMLView.as_view(), name='register'),

    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('', user_views.dashboard, name='dashboard'),

    path('accounts/', include('accounts.front_urls')),
    path('charges/', include('charges.front_urls')),
    path('payments/', include('payments.front_urls')),
]
