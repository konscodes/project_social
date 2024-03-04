from datetime import datetime
from typing import Optional

from pydantic import BaseModel, validator
from sqlmodel import Field, SQLModel


# Define the SQLModel for the Post table
class PostBase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int
    date_created: datetime = Field(default=datetime.now())
    published: Optional[bool] = Field(default=True)


# Define the schema for a general response
class PostLimited(BaseModel):
    id: int
    title: str
    content: str
    user_id: int
    date_created: datetime


# Define the schema for a response upon post creation
class CreatePost(BaseModel):
    message: str = 'Successfully created post'
    id: int
    title: str


# Define the schema for a response upon post creation
class UpdatePost(BaseModel):
    message: str = 'Successfully updated post'
    id: int
    title: str


# Define the SQLModel for the User table
class UserBase(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=1)
    email: str = Field(min_length=1, default=None, unique=True)
    password: str = Field(min_length=1)
    date_created: datetime = Field(default=datetime.now(), nullable=False)

    # TODO
    # Name field is accepted as empty which is not good, need to fix
    # validator doesnt work as expected
    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v.strip() == '':
            raise ValueError('Name cannot be an empty string')
        return v


# Define the schema for a general response
class UserLimited(BaseModel):
    id: int
    name: str
    email: str


# Define the schema for a response upon user creation
class CreateUser(BaseModel):
    message: str = 'Successfully created user'
    id: int
    name: str
    email: str


# Define the schema for a response upon user creation
class UpdateUser(BaseModel):
    message: str = 'Successfully updated user'
    id: int
    name: str
    email: str
