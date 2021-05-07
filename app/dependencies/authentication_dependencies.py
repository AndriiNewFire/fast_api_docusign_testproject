from datetime import datetime, timedelta
from typing import Optional

from jose import jwt
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/api/token')

SECRET_KEY = 'a7b9e551df964711519796d9f21d533b79e17958e887f55a94668bc6852e8ea9'
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    excoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return excoded_jwt
