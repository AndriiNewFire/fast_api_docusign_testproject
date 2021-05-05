from fastapi import Depends
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter
from sqlalchemy.orm import Session

from db.user_and_documents_management import crud
from schemes import user_and_documents_schemes
from dependencies.db import get_db

router = InferringRouter()


@cbv(router)
class DocumentsManagement:

    @router.post('/documents/add', response_model=user_and_documents_schemes.Document)
    def create_document_for_user(self, user_id: int,
                                 document: user_and_documents_schemes.DocumentCreate,
                                 db: Session = Depends(get_db)):

        return crud.create_user_document(db=db, document=document, user_id=user_id)
