from fastapi import (FastAPI, Form, Cookie, Request,
                     HTTPException)
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from app.services import launch

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")

# In-memory user database for demonstration purposes
fake_users_db = {
    "user1": {"username": "user1", "hashed_password": "password1"},
    "user2": {"username": "user2", "hashed_password": "password2"}
}

def get_user(db, username: str):
    """Fetch user from the database."""
    return db.get(username)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Simulated password verification."""
    return plain_password == hashed_password

@app.get("/", response_class=HTMLResponse)
async def read_login(request: Request):
    """Render the login page."""
    return templates.TemplateResponse("login.html", {"request": request})


@app.post("/login", response_class=HTMLResponse)
async def handle_login(
    username: str = Form(...),
    password: str = Form(...),
):
    """Handle login form submission."""
    user = get_user(fake_users_db, username)
    if user is None or not verify_password(password, user["hashed_password"]):
        return HTMLResponse(
            content="<h2>Invalid credentials! Please <a href='/'>try again</a>.</h2>",
            status_code=401,
        )

    response = RedirectResponse(url="/launch", status_code=303)
    response.set_cookie(key="username", value=username)
    return response

@app.get("/launch", response_class=HTMLResponse)
async def launch_page(request: Request, username: str = Cookie(None)):
    """Render the launch campaign page."""
    if username is None or username not in fake_users_db:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("launch.html", {"request": request})

@app.post("/launch", response_class=HTMLResponse)
async def handle_launch(username: str = Cookie(None)):
    """Handle launching a campaign."""
    if username is None or username not in fake_users_db:
        return RedirectResponse(url="/", status_code=303)

    # Trigger the campaign logic in services.py
    launch()

    # Redirect to the dashboard after campaign launch
    return RedirectResponse(url="/dashboard", status_code=303)

@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(request: Request, username: str = Cookie(None)):
    """Render the dashboard page."""
    if username is None or username not in fake_users_db:
        return RedirectResponse(url="/")
    return templates.TemplateResponse("dashboard.html", {"request": request})