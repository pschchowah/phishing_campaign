from fastapi import FastAPI, Form, Depends, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from fastapi import Cookie, Response

app = FastAPI()

# Mount static files (for CSS)
app.mount("/static", StaticFiles(directory="static"),
          name="static")

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"],
                           deprecated="auto")

# Fake user database for demonstration
fake_users_db = {
    "user": {
        "username": "user",
        "full_name": "User Example",
        "email": "user@example.com",
        "hashed_password": pwd_context.hash("pass"),
    }
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# HTML templates
login_html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Login Page</title>
        <style>
            body { font-family: Arial, sans-serif; }
            .container { max-width: 300px; margin: auto; padding: 20px; }
            input { width: 100%; padding: 10px; margin: 5px 0; }
            button { width: 100%; padding: 10px; }
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Login</h2>
            <form action="/login" method="post">
                <input type="text" name="username" placeholder="Username" required>
                <input type="password" name="password" placeholder="Password" required>
                <button type="submit">Login</button>
            </form>
        </div>
    </body>
</html>
"""

launch_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Launch Campaign</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 300px; margin: auto; padding: 20px; text-align: center; }
        button { width: 100%; padding: 10px; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Launch Campaign Page</h2>
        <form action="/launch" method="post">
            <button type="submit">Launch Campaign</button>
        </form>
    </div>
</body>
</html>
"""

dashboard_html = """
<!DOCTYPE html>
<html>
<head>
    <title>Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; }
        .container { max-width: 600px; margin: auto; padding: 20px; text-align: center; }
        h2 { margin-bottom: 20px; }
        p { font-size: 18px; }
        a { display: inline-block; margin-top: 20px; padding: 10px 20px; background-color: #007BFF; color: white; text-decoration: none; border-radius: 5px; }
        a:hover { background-color: #0056b3; }
    </style>
</head>
<body>
    <div class="container">
        <h2>Dashboard</h2>
        <p>Welcome to your dashboard!</p>
        <a href="/">Logout</a>
    </div>
</body>
</html>
"""


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password,
                              hashed_password)


def get_user(db, username: str):
    if username in db:
        return db[username]
    return None


@app.get("/", response_class=HTMLResponse)
async def read_login():
    return login_html


@app.post("/login", response_class=HTMLResponse)
async def handle_login(
    username: str = Form(...),
    password: str = Form(...),
):
    user = get_user(fake_users_db, username)
    if user is None or not verify_password(password, user["hashed_password"]):
        return HTMLResponse(
            content="<h2>Invalid credentials! Please <a href='/'>try again</a>.</h2>",
            status_code=401
        )

    # Redirect with cookie set properly
    response = RedirectResponse(url="/launch", status_code=303)
    response.set_cookie(key="username", value=username)
    return response


@app.get("/launch", response_class=HTMLResponse)
async def launch_page(username: str = Cookie(None)):
    if username is None or username not in fake_users_db:
        return RedirectResponse(
            url="/")
    return launch_html


@app.post("/launch", response_class=HTMLResponse)
async def handle_launch(username: str = Cookie(None)):
    if username is None or username not in fake_users_db:
        return RedirectResponse(
            url="/",
            status_code=303  # Use 303 for redirect after POST
        )
    return RedirectResponse(
        url="/dashboard",
        status_code=303  # Use 303 for redirect after POST
    )


@app.get("/dashboard", response_class=HTMLResponse)
async def get_dashboard(username: str = Cookie(None)):
    if username is None or username not in fake_users_db:
        return RedirectResponse(
            url="/")
    return dashboard_html

