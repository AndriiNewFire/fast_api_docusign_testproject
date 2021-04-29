from fastapi import Depends, HTTPException
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from dependencies.db import session_local, engine
from db import crud, models, schemas

router = InferringRouter()

models.Base.metadata.create_all(bind=engine)


@cbv(router)
class UserAndDocumentsManagement:

    def get_db(self):
        db = session_local()
        try:
            yield db
        finally:
            db.close()

    @router.post('/users/', response_model=schemas.User)
    def create_user(self, user: schemas.UserCreate, db: Session = Depends(get_db)):
        db_user = crud.get_user_by_email(db, email=user.email)
        if db_user:
            raise HTTPException(status_code=400, detail='Email exists')
        return crud.create_user(db=db, user=user)

    @router.get('/users/', response_model=list[schemas.User])
    def read_users(self, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        users = crud.get_users(db, skip=skip, limit=limit)
        return users
