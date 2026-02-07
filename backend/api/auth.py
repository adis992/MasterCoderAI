"""
MasterCoderAI - Auth API
Authentication with JWT and database integration
"""
from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
import os
import sys

# Fix imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

router = APIRouter(prefix="/auth", tags=["auth"])

# Security
SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24 hours

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Models
class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        is_admin: bool = payload.get("is_admin", False)
        return {"username": username, "id": user_id, "is_admin": is_admin}
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.post("/login", response_model=Token)
async def login(request: LoginRequest):
    from db.database import database
    from api.models import users
    from api.system import SERVER_INITIALIZATION_STATE
    
    # Get user from database
    query = users.select().where(users.c.username == request.username)
    user = await database.fetch_one(query)
    
    if not user or not check_password_hash(user["hashed_password"], request.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    # Check if user is admin or if server is ready for regular users
    if not user["is_admin"]:
        if not SERVER_INITIALIZATION_STATE.get("user_access_enabled", False):
            raise HTTPException(
                status_code=503, 
                detail="System is still initializing. Please wait for admin to complete setup. Try again in a few minutes."
            )
    
    token = create_access_token({
        "sub": user["username"],
        "id": user["id"],
        "is_admin": user["is_admin"]
    })
    return {"access_token": token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    return verify_token(token)
