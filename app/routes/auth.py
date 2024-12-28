from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.config import settings
import httpx

router = APIRouter()

# Google OAuth URLs
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"

@router.get("/login")
def login_with_google():
    params = {
        "client_id": settings.GOOGLE_CLIENT_ID,
        "redirect_uri": settings.CALLBACK_URL,
        "response_type": "code",
        "scope": "https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile",
        "access_type": "offline",
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{'&'.join([f'{key}={value}' for key, value in params.items()])}"
    return RedirectResponse(auth_url)

@router.get("/callback")
async def callback(code: str):
    try:
        # Exchange code for token
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "client_id": settings.GOOGLE_CLIENT_ID,
                    "client_secret": settings.GOOGLE_CLIENT_SECRET,
                    "redirect_uri": settings.CALLBACK_URL,
                    "grant_type": "authorization_code",
                    "code": code,
                },
            )
        token_response.raise_for_status()
        tokens = token_response.json()

        # Get user info
        async with httpx.AsyncClient() as client:
            userinfo_response = await client.get(
                GOOGLE_USERINFO_URL,
                headers={"Authorization": f"Bearer {tokens['access_token']}"},
            )
        userinfo_response.raise_for_status()
        user_info = userinfo_response.json()

        # Redirect to dashboard with user name
        user_name = user_info.get("name", "User")
        return RedirectResponse(f"/auth/dashboard?user_name={user_name}")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


templates = Jinja2Templates(directory="app/templates")

@router.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, user_name: str = "User"):
    return templates.TemplateResponse("dashboard.html", {"request": request, "user_name": user_name})

@router.get("/logout", response_class=HTMLResponse)
def logout():
    return RedirectResponse("/")
