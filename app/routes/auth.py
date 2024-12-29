from fastapi import APIRouter, HTTPException
from fastapi.responses import RedirectResponse
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request
from app.config import settings
import httpx
from app.config import supabase


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

        # Prepare user data for Supabase
        user_data = {
            "email": user_info.get("email"),
            "full_name": user_info.get("name"),
            "avatar_url": user_info.get("picture"),
            "auth_provider": "google",
            "auth_provider_id": user_info.get("id"),
            "last_sign_in": "now()",  # Menggunakan fungsi NOW() dari PostgreSQL
            "updated_at": "now()"
        }

        # Insert atau update user ke Supabase
        try:
            response = supabase.table("users").upsert(
                user_data,
                on_conflict="email"  # Menggunakan email sebagai unique constraint
            ).execute()
            
            if hasattr(response, 'error') and response.error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Failed to save user data: {response.error.message}"
                )
                
            # Ambil data user yang baru disimpan
            user = response.data[0] if response.data else None
            
            if not user:
                raise HTTPException(
                    status_code=500,
                    detail="Failed to retrieve saved user data"
                )

            # Redirect ke dashboard dengan user name
            return RedirectResponse(
                f"/auth/dashboard?user_name={user.get('full_name', 'User')}&user_id={user.get('id')}"
            )

        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Database error: {str(e)}"
            )

    except httpx.HTTPError as e:
        raise HTTPException(
            status_code=400,
            detail=f"OAuth error: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Server error: {str(e)}"
        )



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
