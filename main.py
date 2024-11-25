from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import auth
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi import Request

templates = Jinja2Templates(directory="app/templates")

app = FastAPI()

@app.get("/", response_class=HTMLResponse)
def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(auth.router, prefix="/auth")
