from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer

AUTH_BASE_URL = "https://auth.delphai.com/auth/realms/delphai/protocol/openid-connect"

OAuth2Token = Depends(
    OAuth2AuthorizationCodeBearer(
        authorizationUrl=f"{AUTH_BASE_URL}/auth",
        tokenUrl=f"{AUTH_BASE_URL}/token",
    )
)
