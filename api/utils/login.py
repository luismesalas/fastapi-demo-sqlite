from fastapi import Header, HTTPException, status

BEARER_PREFIX = "Bearer "
FAKE_VALID_TOKEN = "ABRE_LA_PUERTA_NINIA"


def check_token_format(authorization):
    if not authorization or not authorization.startswith(BEARER_PREFIX):
        raise ValueError("Missing or invalid access token format")
    return authorization[len(BEARER_PREFIX):]


def validate_access_token(authorization: str = Header(...)):
    # We keep only the string after 'Bearer'
    access_token = check_token_format(authorization)

    if access_token != FAKE_VALID_TOKEN:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired access token")
