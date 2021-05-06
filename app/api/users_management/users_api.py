from datetime import timedelta

from fastapi import Depends, HTTPException, status
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from db.user_and_documents_management import crud
from db.user_and_documents_management.authentication import get_current_user, authenticate_user
from db.user_and_documents_management.crud import get_user_by_email, delete_user
from dependencies.authentication_dependencies import ACCESS_TOKEN_EXPIRE_MINUTES, create_access_token
from schemes import user_and_documents_schemes
from schemes.user_and_documents_schemes import User
from dependencies.db import get_db


router = InferringRouter()


@cbv(router)
class UserAndDocumentsManagement:

    @router.get('/api/testing/get_current_user/')
    def test(self, current_user: User = Depends(get_current_user)):
        return current_user

    @router.post("/api/token")
    async def login(self, form_data: OAuth2PasswordRequestForm = Depends(),
                    db: Session = Depends(get_db)):
        user = authenticate_user(form_data.username, form_data.password, db)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(data={'sub': user.email}, expires_delta=access_token_expires)

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

    @router.delete('/users/{user_email}')
    def delete_user(self, user_email: str, db: Session = Depends(get_db), ):

        user = get_user_by_email(db, email=user_email)
        if not user:
            raise HTTPException(status_code=404, detail="User not found, please register")
        return delete_user(db, user)

    # Endpoint to create user account
    @router.post('/users/', response_model=user_and_documents_schemes.User)
    def create_user(self, user: user_and_documents_schemes.UserCreate,
                    db: Session = Depends(get_db)):

        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail='Email exists')
        return crud.create_user(db=db, user=user)
