from msal import ConfidentialClientApplication
from fastapi import HTTPException
import config

msal_app = ConfidentialClientApplication(
    config.CLIENT_ID,
    authority=config.AUTHORITY,
    client_credential=config.CLIENT_SECRET
)

def get_auth_url():
    return msal_app.get_authorization_request_url(
        scopes=["openid", "profile", "email"],
        redirect_uri=config.REDIRECT_URI
    )

def acquire_token_by_code(auth_code: str):
    token_response = msal_app.acquire_token_by_authorization_code(
        code=auth_code,
        scopes=["openid", "profile", "email"],
        redirect_uri=config.REDIRECT_URI
    )
    if "error" in token_response:
        raise HTTPException(status_code=400, detail=token_response.get("error_description"))
    return token_response