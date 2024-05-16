from starlette.responses import RedirectResponse
from fastapi import HTTPException, status, APIRouter, Request, Response, Form
from typing import Optional, Annotated
from models import User
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from fastapi.responses import HTMLResponse
from sqlalchemy import or_
from dependencies import SECRET_KEY, ALGORITHM, templates, db_dependency, form_data_dependency
from pydantic import EmailStr


router = APIRouter(
    prefix="/auth",
    responses={401: {"user": "Not authorized"}}
)

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")



class LoginForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.username: Optional[str] = None
        self.password: Optional[str] = None

    async def create_oauth_form(self):
        form = await self.request.form()
        self.username = form.get("username")
        self.password = form.get("password")


def hash_password(password: str, username: str) -> str:
    password = f'{password}@{username}'
    return bcrypt_context.hash(password)


def authenticate_user(username: str, password: str, db):
    user = db.query(User).filter(User.username == username).first()
    if not user:
        return False
    plain_password = f'{password}@{username}'
    if not bcrypt_context.verify(plain_password, user.password):
        return False
    return user


def create_access_token(user, exp: timedelta):
    payload = {
        "sub": user.username,
        "id": user.id,
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "exp": exp
        }
    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(request: Request):
    try:
        token = request.cookies.get("access_token", None)
        if token is None:
            return None
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub", None)
        user_id: int = payload.get("id", None)
        is_active: bool = payload.get("is_active", None)
        is_admin: bool = payload.get("is_admin", None)
        if username is None or user_id is None:
            logout(request)
        return {"username": username, "id": user_id, "is_active": is_active, "is_admin": is_admin}
    except JWTError:
        return None


@router.post("/token")
async def login_for_access_token(response: Response, form_data: form_data_dependency, db: db_dependency):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        return False
    token_expires = datetime.now(timezone.utc) + timedelta(hours=1)
    token = create_access_token(user, exp=token_expires)
    response.set_cookie(key="access_token", value=token, httponly=True, expires=token_expires, secure=True)
    return True


@router.get("/", response_class=HTMLResponse)
async def authentication_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@router.post("/", response_class=HTMLResponse)
async def login(request: Request, db: db_dependency):
    try:
        form = LoginForm(request)
        await form.create_oauth_form()
        response = RedirectResponse(url="/todos", status_code=status.HTTP_302_FOUND)
        validate_user_cookie = await login_for_access_token(response=response, form_data=form, db=db)
        if not validate_user_cookie:
            msg = "Incorrect Username or Password"
            return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
        return response
    except HTTPException:
        msg = "Unknown Error"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})


@router.get("/logout")
async def logout(request: Request):
    msg = "Logout Successful"
    response = templates.TemplateResponse("login.html", {"request": request, "msg": msg})
    response.delete_cookie(key="access_token")
    return response


@router.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/register", response_class=HTMLResponse)
async def register_user(
        request: Request,
        db: db_dependency,
        username: Annotated[str, Form(...)],
        email: Annotated[EmailStr, Form(...)],
        password: Annotated[str, Form(...)],
        password_confirm: Annotated[str, Form(...)]
    ):
    validation = db.query(User).filter(or_(User.username == username, User.email == email)).first()
    if password != password_confirm:
        msg = "Password are not same"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
    elif validation is not None:
        msg = "User already exists"
        return templates.TemplateResponse("register.html", {"request": request, "msg": msg})
    else:
        user_model = User()
        user_model.username = username
        user_model.email = email
        password = hash_password(password, username)
        user_model.password = password
        db.add(user_model)
        db.commit()
        msg = "User successfully created"
        return templates.TemplateResponse("login.html", {"request": request, "msg": msg})
