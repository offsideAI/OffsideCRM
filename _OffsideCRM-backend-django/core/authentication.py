from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from ninja.security import APIKeyHeader
from ninja.errors import HttpError
from .models import BlacklistedAccessToken

class JWTAuth(APIKeyHeader):
    param_name = "Authorization"

    def authenticate(self, request, key):
        try:
            # key is the full Authorization header, e.g. "JWT <token>"
            if not key:
                return None
            
            parts = key.split()
            if len(parts) != 2 or parts[0] not in ["Bearer", "JWT"]:
                return None
            
            token = parts[1]

            # Instantiate JWTAuthentication class from DRF SimpleJWT
            jwt_auth = JWTAuthentication()
            # Simulate DRF's request to have the token in the header
            validated_token = jwt_auth.get_validated_token(token)
            
            # Check against custom blacklist
            jti = validated_token.get('jti')
            if BlacklistedAccessToken.objects.filter(token_jti=jti).exists():
                raise HttpError(401, 'Token is blacklisted')

            # Attempt to get the user from the validated token
            user = jwt_auth.get_user(validated_token)
            if user is not None and user.is_active:
                return user
            return None
        except (InvalidToken, TokenError) as e:
            raise HttpError(401, 'Invalid or expired token')
        except Exception as e:
            # You might want to log this exception.
            raise HttpError(401, 'Authentication failed')
