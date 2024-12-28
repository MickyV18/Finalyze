import os
from dotenv import load_dotenv
from supabase import create_client
from dotenv import load_dotenv
import os
from fastapi.templating import Jinja2Templates

load_dotenv()

class Settings:
    GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
    CALLBACK_URL = os.getenv("CALLBACK_URL")

settings = Settings()

# Existing configs
templates = Jinja2Templates(directory="app/templates")

# Supabase config
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)