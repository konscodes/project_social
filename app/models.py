from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


# Define the SQLModel for the Post table
class Post(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    content: str
    user_id: int
    date_created: datetime = Field(default=datetime.now())
