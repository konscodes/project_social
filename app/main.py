from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from .database import get_session
from .models import Post

app = FastAPI()


# Root route
@app.get('/')
def root():
    return {'message': 'Hello World'}


# Get all posts
@app.get('/posts/', response_model=list[Post])
def read_posts(session: Session = Depends(get_session)):
    statement = select(Post)
    return session.exec(statement).all()


# Get a specific post
@app.get('/posts/{post_id}', response_model=Post)
def read_post(post_id: int, session: Session = Depends(get_session)):
    statement = select(Post).where(Post.id == post_id)
    post = session.exec(statement).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    return post


# Create a new post
@app.post('/posts/', response_model=dict)
def create_post(post: Post, session: Session = Depends(get_session)):
    session.add(post)
    session.commit()
    return {'message': f'Successfully created post {post.title}'}


# Update a post
@app.put('/posts/{post_id}', response_model=dict)
def update_post(post_id: int,
                data: Post,
                session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(post, key, value)
    session.add(post)
    session.commit()
    return {'message': f'Successfully updated post {post_id}'}


# Delete a post
@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, session: Session = Depends(get_session)):
    post = session.get(Post, post_id)
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    session.delete(post)
    session.commit()
    return None
