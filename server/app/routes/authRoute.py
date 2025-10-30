import os
import requests
from fastapi import APIRouter, HTTPException

LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET")

router = APIRouter(prefix="/auth/linkedin", tags=["LinkedIn OAuth"])

@router.post("/token")
def get_access_token(data: dict):
    code = data.get("code")
    redirect_uri = data.get("redirect_uri")

    token_url = "https://www.linkedin.com/oauth/v2/accessToken"
    payload = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
        "client_id": LINKEDIN_CLIENT_ID,
        "client_secret": LINKEDIN_CLIENT_SECRET,
    }

    res = requests.post(token_url, data=payload)
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail=res.json())

    return res.json()

@router.get("/me")
def get_user_info(authorization: str):
    token = authorization.replace("Bearer ", "")
    headers = {"Authorization": f"Bearer {token}"}
    res = requests.get("https://api.linkedin.com/v2/userinfo", headers=headers)
    if res.status_code != 200:
        raise HTTPException(status_code=400, detail=res.json())
    return res.json()
