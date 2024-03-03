from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from .database import create_tables, get_session
from .models import CreatePost, PostBase, PostLimited, UpdatePost

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
