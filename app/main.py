from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from .database import create_tables, get_session
from .models import (
    CreatePost,
    CreateUser,
    PostBase,
    PostLimited,
    UpdatePost,
    UpdateUser,
    UserBase,
    UserLimited,
)

create_tables()

app = FastAPI()


# Root route
@app.get('/')
def root():
    return {'message': 'Hello World'}


# Get all posts
@app.get('/posts/', response_model=list[PostLimited])
def read_posts(session: Session = Depends(get_session)):
    statement = select(PostBase)
    return session.exec(statement).all()


# Get a specific post
@app.get('/posts/{post_id}', response_model=PostBase)
def read_post(post_id: int, session: Session = Depends(get_session)):
    statement = select(PostBase).where(PostBase.id == post_id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    return post


# Create a new post
@app.post('/posts/', response_model=CreatePost)
def create_post(post: PostBase, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    return post


# Update a post
@app.put('/posts/{post_id}', response_model=UpdatePost)
def update_post(post_id: int,
                data: PostBase,
                session: Session = Depends(get_session)):
    post = session.get(PostBase, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    session.add(post)
    session.commit()
    return post


# Delete a post
@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(PostBase, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    session.delete(post)
    session.commit()
    return None


# Get all users
@app.get('/users/', response_model=list[UserLimited])
def read_users(session: Session = Depends(get_session)):
    statement = select(UserBase)
    return session.exec(statement).all()


# Get a specific user
@app.get('/users/{user_id}', response_model=UserBase)
def read_user(user_id: int, session: Session = Depends(get_session)):
    statement = select(UserBase).where(UserBase.id == user_id)
    user = session.exec(statement).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    return user


# Create a new user
@app.post('/users/', response_model=CreateUser)
def create_user(user: UserBase, session: Session = Depends(get_session)):
    session.add(user)
    session.commit()
    return user


# Update a user
@app.put('/users/{user_id}', response_model=UpdateUser)
def update_user(user_id: int,
                data: UserBase,
                session: Session = Depends(get_session)):
    user = session.get(UserBase, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    return user


# Delete a user
@app.delete('/users/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user = session.get(UserBase, user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='User not found')
    session.delete(user)
    session.commit()
    return None
