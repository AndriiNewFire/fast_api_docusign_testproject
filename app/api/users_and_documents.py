from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from db.user_and_documents_management import crud
from schemes import user_and_documents_schemes
from dependencies.db import get_db


router = InferringRouter()


@cbv(router)
class UserAndDocumentsManagement:

    @router.post('/users/', response_model=user_and_documents_schemes.User)
    def create_user(self, user: user_and_documents_schemes.UserCreate,
                    db: Session = Depends(get_db)):
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail='Email exists')
        return crud.create_user(db=db, user=user)

    @router.get('/users/', response_model=list[user_and_documents_schemes.User])
    def read_users(self, skip: int = 0,
                   limit: int = 10,
                   db: Session = Depends(get_db)):

        users = crud.get_users(db, skip=skip, limit=limit)
        return users

    @router.post('/documents/add', response_model=user_and_documents_schemes.Document)
    def create_document_for_user(self, user_id: int,
                                 document: user_and_documents_schemes.DocumentCreate,
                                 db: Session = Depends(get_db)):

        return crud.create_user_document(db=db, document=document, user_id=user_id)
