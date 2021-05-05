from fastapi import Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from db.user_and_documents_management.crud import get_user_by_email
from dependencies.db import get_db
from dependencies.authentication_dependencies import pwd_context, oauth2_scheme, SECRET_KEY, ALGORITHM
from exceptions.exceptions import credentials_exception
from schemes.authentication_scheme import TokenData


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(username: str,
                      db: Session = Depends(get_db)):

    user = get_user_by_email(db, email=username)
    return user


async def get_current_user(db: Session = Depends(get_db),
                           token: str = Depends(oauth2_scheme)):

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
        username: str = payload.get('sub')
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)

    except JWTError:
        raise credentials_exception

    user = get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception

    return user
