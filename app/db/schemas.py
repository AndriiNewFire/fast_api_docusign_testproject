from datetime import datetime

from pydantic import BaseModel

"""
Declared also pydantic version of the structure for testing purposes
"""


class DocumentBase(BaseModel):
    title: str


class DocumentCreate(DocumentBase):
    pass


class Document(DocumentBase):
    id: int
    owner_id: int
    title: str = 'Default Title'

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    documents: list[Document] = []

    class Config:
        orm_mode = True
