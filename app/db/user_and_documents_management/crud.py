from db.user_and_documents_management import models
from schemes import user_and_documents_schemes
from sqlalchemy.orm import Session


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_users(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session, user: user_and_documents_schemes.UserCreate):

    fake_hashed_password = user.password + 'lol'
    db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_documents(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Document).offset(skip).limit(limit).all()


def create_user_document(db: Session, document: user_and_documents_schemes.DocumentCreate, user_id: int):
    db_document = models.Document(**document.dict(), owner_id=user_id)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document
