from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import JWTError, jwt
from pydantic import BaseModel
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Patch: always load .env from backend folder
BACKEND_ENV_PATH = os.path.join(os.path.dirname(__file__), '../../../.env')
load_dotenv(BACKEND_ENV_PATH)
backend_env_path = os.path.join(os.path.dirname(__file__), '../../../backend/.env')
load_dotenv(backend_env_path)

# Hard-code the SECRET_KEY for testing to ensure consistency
SECRET_KEY = "neki_jako_dobar_random_string_za_mastercoderai_2025"
print(f"[DEBUG] Using hardcoded SECRET_KEY, loaded from: {backend_env_path}")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from .db import database
from .models import users

router = APIRouter(prefix="/auth", tags=["auth"])
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class UserCreate(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

@router.post("/register", status_code=201)
async def register(user: UserCreate):
    query = users.select().where(users.c.username == user.username)
    existing = await database.fetch_one(query)
    if existing:
        raise HTTPException(status_code=400, detail="Username taken")
    hashed = pwd_context.hash(user.password)
    insert = users.insert().values(username=user.username, hashed_password=hashed, is_admin=False)
    await database.execute(insert)
    return {"msg": "User created"}

@router.post("/login", response_model=Token)
async def login(user: UserCreate):
    query = users.select().where(users.c.username == user.username)
    db_user = await database.fetch_one(query)
    if not db_user or not pwd_context.verify(user.password, db_user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    data = {"sub": str(db_user["id"]), "username": db_user["username"], "is_admin": db_user["is_admin"]}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    # Spremi token korisniku u bazu
    await database.execute(users.update().where(users.c.id == db_user["id"]).values(last_token=token))
    return {"access_token": token, "token_type": "bearer"}

@router.post("/admin-token", tags=["auth"])
async def admin_token():
    """
    Generate a JWT token for the admin user (for panel bootstrap).
    Only for initial setup, remove or protect in production!
    """
    query = users.select().where(users.c.username == "admin")
    db_user = await database.fetch_one(query)
    if not db_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    data = {"sub": str(db_user["id"]), "username": db_user["username"], "is_admin": db_user["is_admin"]}
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return {"access_token": token, "token_type": "bearer"}

@router.post("/reset-admin", tags=["auth"])
async def reset_admin_password():
    """
    Privremeni endpoint za reset admin lozinke na 'admin'.
    Ukloniti iz produkcije!
    """
    from .models import users
    query = users.select().where(users.c.username == "admin")
    db_user = await database.fetch_one(query)
    if not db_user:
        raise HTTPException(status_code=404, detail="Admin user not found")
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    hashed = pwd_context.hash("admin")
    await database.execute(users.update().where(users.c.username == "admin").values(hashed_password=hashed))
    return {"status": "admin password reset to 'admin'"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print("[DEBUG] Decoded payload:", payload)  # Debug log
        user_id_raw = payload.get("sub")
        if user_id_raw is None:
            raise credentials_exception
        user_id = int(user_id_raw)
    except JWTError as e:
        print("[DEBUG] JWTError:", e)  # Debug log
        raise credentials_exception
    query = users.select().where(users.c.id == user_id)
    print("[DEBUG] Executing query:", query)  # Debug log
    user = await database.fetch_one(query)
    if user is None:
        print("[DEBUG] User not found for ID:", user_id)  # Debug log
        raise HTTPException(status_code=404, detail="User not found")
    return dict(user)

# if __name__ == "__main__":
#     import sys, os
#     sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
#     import asyncio
#     print("Generating admin JWT token...")
#     asyncio.run(print_admin_token())