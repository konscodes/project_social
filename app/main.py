# Import fastapi and create a default test route
import sqlite3
from pathlib import Path
from typing import List, Optional

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic.main import BaseModel

script_path = Path(__file__).parent
project_path = script_path.parent
db_path = project_path / 'db' / 'main.sqlite'

app = FastAPI()


# Utilize pydantic schema to perform automatic type checking of incoming data
class Post(BaseModel):
    id: Optional[int] = None
    title: str
    description: str
    user_id: int


def get_connection():
    connection = sqlite3.connect(db_path)
    return connection


def close_connection(connection: sqlite3.Connection):
    connection.close()


@app.get('/', response_class=JSONResponse)
def root():
    '''Returns Hello world for basic testing'''
    return {'message': 'Hello world!!'}


@app.get('/posts/', response_model=List[Post])
def get_posts(connection: sqlite3.Connection = Depends(get_connection)):
    select_posts = '''--sql
    SELECT * from posts;
    '''
    cursor = connection.cursor()
    cursor.execute(select_posts)
    posts = cursor.fetchall()
    cursor.close()

    # Convert fetched posts to a list of Post objects
    post_objects = []
    for post in posts:
        post_objects.append(
            Post(id=post[0],
                 title=post[1],
                 description=post[2],
                 user_id=post[3]))
    return post_objects


@app.get('/posts/{post_id}', response_model=Post | dict)
def get_post(post_id: int,
             short: bool = True,
             connection: sqlite3.Connection = Depends(get_connection)):
    select_posts = '''--sql
    SELECT * from posts WHERE id = ?;
    '''
    cursor = connection.cursor()
    cursor.execute(select_posts, (post_id, ))
    post = cursor.fetchone()
    cursor.close()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Post not found')
    post_object = Post(id=post[0],
                       title=post[1],
                       description=post[2],
                       user_id=post[3])
    if short:
        return {'title': post_object.title}
    return post_object


@app.post('/posts/', status_code=status.HTTP_201_CREATED)
def create_post(post: Post,
                connection: sqlite3.Connection = Depends(get_connection)):
    create_post_query = '''--sql
    INSERT INTO posts (title, description, user_id) VALUES (?, ?, ?);
    '''
    cursor = connection.cursor()
    cursor.execute(create_post_query,
                   (post.title, post.description, post.user_id))
    connection.commit()
    cursor.close()
    return {'message': f'Successfully created post {post.title}'}


@app.put('/posts/{post_id}')
def update_post(post_id: int,
                post: Post,
                connection: sqlite3.Connection = Depends(get_connection)):
    update_post_query = '''--sql
    UPDATE posts SET title = ?, description = ?, user_id = ? WHERE id = ?;
    '''
    cursor = connection.cursor()
    cursor.execute(update_post_query,
                   (post.title, post.description, post.user_id, post_id))
    connection.commit()
    cursor.close()
    return {'message': f'Successfully updated post {post_id}'}


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int,
                connection: sqlite3.Connection = Depends(get_connection)):
    delete_post_query = '''--sql
    DELETE FROM posts WHERE id = ?;
    '''
    cursor = connection.cursor()
    cursor.execute(delete_post_query, (post_id, ))
    connection.commit()
    cursor.close()
    return {'message': f'Successfully deleted the post {post_id}'}
