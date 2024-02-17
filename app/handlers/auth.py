"""
AuthHandler
"""
import re
from datetime import datetime, timedelta
from uuid import UUID

import jwt
import pyotp
import pytz

from app.config import settings
from app.exceptions.auth import InvalidTokenException
from app.libs.consts.enums import ExpireTime, TokenScope
from app.schemas.auth import JWTPayload
from app.schemas.user import User


class AuthHandler:
    """AuthHandler"""

    def __init__(self):
        self._token_expire_time = ExpireTime.ONE_DAY.value * 3  # 3 days

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

    def generate_jwt_token(self, payload: JWTPayload) -> str:
        """
        Generate JWT token
        :param payload:
        :return:
        """
        token = jwt.encode(
            payload=payload.model_dump(),
            key=settings.JWT_SECRET,
            algorithm="HS512"
        )
        return token

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
            exp=expiration_time,
            scope=TokenScope.ACCESS
        )
        return self.generate_jwt_token(payload=payload)

    def generate_2fa_token(self, user: User) -> str:
        """
        Generate 2fa token
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
            exp=expiration_time,
            scope=TokenScope.TWO_FACTOR_AUTH
        )
        return self.generate_jwt_token(payload=payload)

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

    @staticmethod
    def generate_otp_secret() -> str:
        """
        Generate OTP secret
        :return:
        """
        return pyotp.random_base32()

    @staticmethod
    def verify_otp(secret: str, otp: str) -> bool:
        """
        Verify OTP
        :param secret:
        :param otp:
        :return:
        """
        if not secret or not otp:
            return False
        return pyotp.TOTP(secret).verify(otp)

    @staticmethod
    def verify_new_otp(secret: str, previous_otp: str, otp: str) -> bool:
        """
        Verify OTP
        verify previous and current otp
        :param secret:
        :param previous_otp:
        :param otp:
        :return:
        """
        totp = pyotp.TOTP(secret)
        now = datetime.now(tz=pytz.UTC)
        return totp.verify(otp=previous_otp, for_time=now - timedelta(seconds=30)) and totp.verify(otp=otp, for_time=now)

    @staticmethod
    def generate_otp_uri(user_id: UUID, secret: str) -> str:
        """
        Generate OTP uri
        :param user_id:
        :param secret:
        :return:
        """
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=str(user_id),
            issuer_name=settings.APP_FQDN
        )
