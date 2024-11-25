from fastapi import APIRouter, HTTPException
from fastapi import Form
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

@router.post("/login")
def process_login(email: str = Form(...), password: str = Form(...)):
    # Cari user berdasarkan email
    response = supabase.table("users").select("*").eq("email", email).execute()
    if not response.data:
        raise HTTPException(status_code=400, detail="Invalid email or password")

    user = response.data[0]

    # Verifikasi password
    if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
        raise HTTPException(status_code=400, detail="Invalid email or password")

    return {"message": f"Welcome back, {user['username']}!"}



from app.config import supabase
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, status
import bcrypt

from app.config import supabase
from fastapi.responses import RedirectResponse
from fastapi import HTTPException, status
import bcrypt

@router.post("/register")
def process_register(
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...)
):
    # Validasi password
    if password != confirm_password:
        raise HTTPException(status_code=400, detail="Passwords do not match")

    # Hash password
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    # Simpan ke Supabase
    try:
        response = supabase.table("users").insert({
            "username": username,
            "email": email,
            "password": hashed_password,
        }).execute()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error creating user: {e}")

    # Redirect ke halaman login setelah registrasi berhasil
    return RedirectResponse(url="/auth/login-page", status_code=status.HTTP_302_FOUND)



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

        return {
            "access_token": tokens["access_token"],
            "refresh_token": tokens.get("refresh_token"),
            "user_info": user_info,
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/manual-login")
def manual_login(username: str = Form(...), password: str = Form(...)):
    # Validasi username dan password di sini
    if username == "admin" and password == "password123":
        return {"message": "Login successful"}
    else:
        raise HTTPException(status_code=401, detail="Invalid credentials")


templates = Jinja2Templates(directory="app/templates")

@router.get("/login-page", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.get("/register-page", response_class=HTMLResponse)
def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})