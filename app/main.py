from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from .database import create_db_and_tables, get_session
from .models import (
    Post,
    PostCreate,
    PostRead,
    PostUpdate,
    User,
    UserCreate,
    UserRead,
    UserUpdate,
)

create_db_and_tables()

app = FastAPI()


# Root route
@app.get('/')
def root():
    return {'message': 'Hello World'}


# Get all posts
@app.get('/posts/', response_model=list[PostRead])
def read_posts(session: Session = Depends(get_session)):
    db_posts = session.exec(select(Post)).all()
    return db_posts


# Get a specific post
@app.get('/posts/{post_id}', response_model=PostRead)
def read_post(post_id: int, session: Session = Depends(get_session)):
    statement = select(Post).where(Post.post_id == post_id)
    db_post = session.exec(statement).first()
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    return db_post


# Create a new post
@app.post('/posts/', response_model=PostRead)
def create_post(post: PostCreate, session: Session = Depends(get_session)):
    db_post = Post.model_validate(post)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


# Update a post
@app.patch('/posts/{post_id}', response_model=PostRead)
def update_post(post_id: int,
                post: PostUpdate,
                session: Session = Depends(get_session)):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    post_data = post.model_dump(exclude_unset=True)
    db_post.sqlmodel_update(post_data)
    session.add(db_post)
    session.commit()
    session.refresh(db_post)
    return db_post


# Delete a post
@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    db_post = session.get(Post, post_id)
    if not db_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    session.delete(db_post)
    session.commit()
    return None


# Get all users
@app.get('/users/', response_model=list[UserRead])
def read_users(session: Session = Depends(get_session)):
    db_users = session.exec(select(User)).all()
    return db_users


# Get a specific user
@app.get('/users/{user_id}', response_model=UserRead)
def read_user(user_id: int, session: Session = Depends(get_session)):
    statement = select(User).where(User.user_id == user_id)
    db_user = session.exec(statement).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return db_user


# Create a new user
@app.post('/users/', response_model=UserRead)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = User.model_validate(user)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Update a user
@app.patch('/users/{user_id}', response_model=UserRead)
def update_user(user_id: int,
                user: UserUpdate,
                session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    user_data = user.model_dump(exclude_unset=True)
    db_user.sqlmodel_update(user_data)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user


# Delete a user
@app.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    db_user = session.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    session.delete(db_user)
    session.commit()
    return None
