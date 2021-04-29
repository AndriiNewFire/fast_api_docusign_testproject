from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from db import crud, schemas
from dependencies.db import get_db


router = InferringRouter()


@cbv(router)
class UserAndDocumentsManagement:

    @router.post('/users/', response_model=schemas.User)
    def create_user(self, user: schemas.UserCreate,
                    db: Session = Depends(get_db)):

        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail='Email exists')
        return crud.create_user(db=db, user=user)

    @router.get('/users/', response_model=list[schemas.User])
    def read_users(self, skip: int = 0,
                   limit: int = 10,
                   db: Session = Depends(get_db)):

        users = crud.get_users(db, skip=skip, limit=limit)
        return users

    @router.post('/documents/add', response_model=schemas.Document)
    def create_document_for_user(self, user_id: int,
                                 document: schemas.DocumentCreate,
                                 db: Session = Depends(get_db)):

        return crud.create_user_document(db=db, document=document, user_id=user_id)
