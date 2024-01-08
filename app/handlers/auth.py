"""
AuthHandler
"""
import re
from datetime import datetime, timedelta

import pytz

from app.config import settings
from app.exceptions.auth import InvalidTokenException
from app.models.auth import JWTPayload
from app.models.user import User

import jwt


class AuthHandler:
    """AuthHandler"""

    def __init__(self):
        self._token_expire_time = 3600

    @staticmethod
    def verify_password_strength(password: str) -> bool:
        """
        Verify password strength
        :param password:
        :return:
        """
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()_+]).{16,}$'
        match = re.match(pattern, password)
        return bool(match)

    def generate_token(self, user: User) -> str:
        """
        Generate token
        :param user:
        :return:
        """
        now = datetime.now(tz=pytz.UTC)
        expiration_time = now + timedelta(seconds=self._token_expire_time)
        payload = JWTPayload(
            iss=settings.APP_NAME,
            uid=user.id,
            sub=user.username,
            name=user.display_name,
            iat=now,
            exp=expiration_time
        )
        token = jwt.encode(
            payload=payload.model_dump(),
            key=settings.JWT_SECRET,
            algorithm="HS512"
        )
        return token

    @staticmethod
    def verify_token(token: str) -> JWTPayload:
        """
        Verify token
        :param token:
        :return:
        """
        try:
            payload = jwt.decode(
                jwt=token,
                key=settings.JWT_SECRET,
                algorithms=["HS512"],
                verify=True,
                issuer=settings.APP_NAME,
                leeway=60  # 60 seconds
            )
            return JWTPayload(**payload)
        except jwt.exceptions.ExpiredSignatureError:
            raise InvalidTokenException("Token has expired")
        except (
            jwt.exceptions.PyJWTError,
            jwt.exceptions.InvalidIssuerError,
            jwt.exceptions.InvalidSignatureError,
            Exception
        ) as e:
            raise InvalidTokenException("Invalid token")
