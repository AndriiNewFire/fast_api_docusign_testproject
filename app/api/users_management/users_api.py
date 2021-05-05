from datetime import datetime, timedelta

from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from db.user_and_documents_management import crud
from schemes import user_and_documents_schemes
from dependencies.db import get_db


from typing import Optional
from passlib.context import CryptContext
from jose import JWTError, jwt
from fastapi import Depends, FastAPI, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel


router = InferringRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='token')

fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}
SECRET_KEY = 'a7b9e551df964711519796d9f21d533b79e17958e887f55a94668bc6852e8ea9'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db,username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    excoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return excoded_jwt

def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)

def fake_decode_token(token):

    user = get_user(fake_users_db, token)
    return user


def fake_hash_password(password: str):
    return "fakehashed" + password


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username = token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@cbv(router)
class UserAndDocumentsManagement:

    @router.get('/testing/users/')
    def test(self, current_user: User = Depends(get_current_user)):
        return current_user

    @router.post("/token")
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends()):
        user = authenticate_user(fake_users_db, form_data.username, form_data.password)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={'sub': user.username}, expires_delta=access_token_expires)

        return {"access_token": access_token, 'token_type': 'bearer'}







    # Endpoint to get all available users
    @router.get('/users/', response_model=list[user_and_documents_schemes.User])
    def get_all_available_user_accounts(self, skip: int = 0,
                                        limit: int = 10,
                                        db: Session = Depends(get_db)):

        users = crud.get_users(db, skip=skip, limit=limit)
        return users

    # Endpoint to get specific user
    @router.get('/users/{user_id}', response_model=user_and_documents_schemes.User)
    def get_all_available_user_accounts(self, user_id: int,
                                        db: Session = Depends(get_db),):

        user = crud.get_user(db, user_id=user_id)

        if not user:
            raise HTTPException(status_code=404, detail="User not found, please register")
        return user

    # Endpoint to create user account
    @router.post('/users/', response_model=user_and_documents_schemes.User)
    def create_user(self, user: user_and_documents_schemes.UserCreate,
                    db: Session = Depends(get_db)):

        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail='Email exists')
        return crud.create_user(db=db, user=user)


