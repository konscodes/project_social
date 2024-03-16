import re
from datetime import datetime
from typing import Optional

from pydantic import EmailStr, validator
from sqlmodel import VARCHAR, Column, Field, SQLModel


# Define the Post model; it is only Pydantic data model
class PostBase(SQLModel):
    title: str = Field(default=None, nullable=False)
    content: str = Field(default=None, nullable=False)
    user_id: int = Field(default=None, nullable=False)
    published: Optional[bool] = Field(default=True, nullable=False)


# Define the Post model that declares the data in the database
# Represents a table; it is both Pydantic model and SQLAlchemy model
class Post(PostBase, table=True):
    post_id: Optional[int] = Field(default=None, primary_key=True)
    date_created: datetime = Field(default=datetime.now())


# Define the schema for Creating a new Post; it is only Pydantic data model
# Declares required fields in addition to fields from Base model
class PostCreate(PostBase):
    pass


# Define the schema for Reading a Post; it is only Pydantic data model
# These additional fields will shape the response model when requeuing a user data
class PostRead(PostBase):
    post_id: int
    date_created: datetime


# Define the schema for Updating a Post; independent Pydantic data model
# We create an independent model since the same fields are required in Base
class PostUpdate(SQLModel):
    title: Optional[str] = None
    content: Optional[str] = None
    user_id: Optional[int] = None
    published: Optional[bool] = None


# Define the User model; it is only Pydantic data model
class UserBase(SQLModel):
    name: str = Field(nullable=False)
    email: EmailStr = Field(sa_column=Column("email", VARCHAR, unique=True))

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if v.strip() == '':
            raise ValueError('Name cannot be an empty string')
        return v


# Define the User model that declares the data in the database
# Represents a table; it is both Pydantic model and SQLAlchemy model
class User(UserBase, table=True):
    user_id: Optional[int] = Field(default=None, primary_key=True)
    date_created: datetime = Field(default=datetime.now(), nullable=False)


# Define the schema for Creating a new User; it is only Pydantic data model
# Declares required fields in addition to fields from Base model
class UserCreate(UserBase):
    password: str = Field(nullable=False, min_length=6)

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        if not re.search(r'\W', v):
            raise ValueError(
                'Password must contain at least one special character')
        if not re.search(r'[A-Z]', v):
            raise ValueError(
                'Password must contain at least one uppercase letter')
        return v


# Define the schema for Reading a User; it is only Pydantic data model
# These additional fields will shape the response model when requeuing a user data
class UserRead(UserBase):
    user_id: int
    date_created: datetime


# Define the schema for Updating a User; independent Pydantic data model
# We create an independent model since the same fields are required in Base
class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
