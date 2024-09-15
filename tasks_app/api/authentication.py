from typing import Tuple
from rest_framework.request import Request
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import Token
from api.models.user_model import User

class JWTCookieAuthentication(JWTAuthentication):
    def authenticate(self, request: Request) -> Tuple[User, Token] | None:
        raw_token = request.COOKIES.get("access")
        if raw_token is None:
            header = self.get_header(request=request)
            if header is None:
                return None
            else:
                raw_token = self.get_raw_token(header=header)

                if raw_token is None:
                    return None
                
        token = self.get_validated_token(raw_token=raw_token)
        
        return self.get_user(validated_token=token), token