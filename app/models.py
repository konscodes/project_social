from datetime import datetime
from typing import Optional

from pydantic.main import BaseModel
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
    title: str
    message: str = 'Successfully created post'


# Define the schema for a response upon post creation
class UpdatePost(BaseModel):
    title: str
    message: str = 'Successfully updated post'
