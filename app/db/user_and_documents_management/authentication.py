from fastapi import Depends
from sqlalchemy.orm import Session
from jose import jwt, JWTError

from db.user_and_documents_management.crud import get_user_by_email
from db.user_and_documents_management.utilities import verify_password
from dependencies.db import get_db
from dependencies.authentication_dependencies import oauth2_scheme, SECRET_KEY, ALGORITHM
from exceptions.exceptions import credentials_exception
from schemes.authentication_scheme import TokenData


def authenticate_user(username: str,
                      password: str,
                      db: Session = Depends(get_db)):

    user = get_user_by_email(db, email=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
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
