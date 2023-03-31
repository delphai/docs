from fastapi import Depends
from fastapi.security import OAuth2AuthorizationCodeBearer


OAuth2Token = Depends(
    OAuth2AuthorizationCodeBearer(
        authorizationUrl="https://auth.delphai.com/auth/realms/delphai/protocol/openid-connect/auth",  # noqa: E501
        tokenUrl="https://auth.delphai.com/auth/realms/delphai/protocol/openid-connect/token",  # noqa: E501
    )
)
