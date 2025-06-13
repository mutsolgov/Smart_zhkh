import time
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from jwt import PyJWKClient, InvalidTokenError

User = get_user_model()

class OIDCAuthentication(BaseAuthentication):
    """
    Аутентификация DRF через Access Token, выданный вашим OIDC Provider (django-oidc-provider).
    Проверяет JWT подпись через JWKS endpoint и возвращает пользователя по sub claim.
    """

    def authenticate(self, request):
        auth_header = request.headers.get('Authorization', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split()[1]
        validated = self._validate_jwt(token)
        sub = validated.get('sub')
        if not sub:
            raise exceptions.AuthenticationFailed("sub claim not present in token")
        try:
            user = User.objects.get(id=sub)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed("User not found")

        return (user, None)

    def _validate_jwt(self, token):
        """
        Проверяет подпись и claims JWT.
        Использует PyJWKClient для получения ключа из JWKS endpoint.
        """
        jwks_url = getattr(settings, 'OIDC_JWKS_ENDPOINT', None)
        if not jwks_url:
            jwks_url = settings.SITE_URL.rstrip('/') + '/openid/jwks/'
        issuer = getattr(settings, 'OIDC_ISSUER', None)
        if not issuer:
            issuer = settings.SITE_URL.rstrip('/') + '/openid'
        audience = getattr(settings, 'OIDC_AUDIENCE', None)
        try:
            jwk_client = PyJWKClient(jwks_url)
            signing_key = jwk_client.get_signing_key_from_jwt(token).key
        except Exception as e:
            raise exceptions.AuthenticationFailed(f"Failed to fetch JWKS or get signing key: {e}")

        options = {
            'verify_aud': audience is not None,
        }
        try:
            decoded = jwt.decode(
                token,
                signing_key,
                algorithms=["RS256"],
                audience=audience,
                issuer=issuer,
                options=options,
            )
        except InvalidTokenError as e:
            raise exceptions.AuthenticationFailed(f"Invalid token: {str(e)}")
        return decoded
