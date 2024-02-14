# Import fastapi and create a default test route
from typing import Optional

import requests
from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from pydantic.main import BaseModel

app = FastAPI()


# Utilize pydantic schema to perform automatic type checking of incoming data
class Post(BaseModel):
    title: str
    description: str
    rating: Optional[int] = None


my_posts = [{
    'title': 'Test 1',
    'description': 'This is a post',
    'rating': 1
}, {
    'title': 'Test 2',
    'description': 'This is a post',
    'rating': 2
}]


@app.get('/')
async def root():
    '''Returns Hello world for basic testing'''
    return {'message': 'Hello world!!'}


@app.get('/items/{item_id}')
def read_item(item_id: int, short: bool = True):
    if not short:
        return {'description': short}
    return {'item_id': item_id}


@app.post('/items/{item_id}')
def create_item(item_id: int):
    return {'message': f'Successfully created item {item_id}'}


@app.get('/posts/')
def get_posts():
    return my_posts


@app.get('/posts/{post_id}')
def get_post(post_id: int, short: bool = True):
    try:
        posts = my_posts[post_id]

        if not short:
            return {'data': posts}
        return {'title': posts['title']}
    except IndexError:
        print('Error: post not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post not found') from IndexError


@app.post('/posts/', status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    my_posts.append(post.model_dump())
    return {'message': f'Successfully created post {post.title}'}


@app.put('/posts/{post_id}')
def update_post(post_id: int, post: Post):
    try:
        my_posts[post_id] = post.model_dump()
        return {'message': f'Successfully updated post {post_id}'}
    except IndexError:
        print('Error: post not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post not found') from IndexError


@app.delete('/posts/{post_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    try:
        my_posts.pop(post_id)
        return {'message': f'Successfully deleted the post {post_id}'}
    except IndexError:
        print('Error: post not found')
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='post not found') from IndexError


async def call_api(endpoint: str, key: str, city: str):
    params = {'key': key, 'q': city}
    response = requests.get(endpoint, params=params)
    if response.status_code == 200:
        data = response.json()
        temperature = data['current']['temp_c']
        humidity = data['current']['humidity']
        return temperature, humidity
    else:
        print(f'Error: {response.status_code} - {response.text}')
        return {'error': response.text}


@app.get('/weather/{city}')
async def get_weather(city: str, short: bool = True):
    '''Return current weather conditions in a given location.

    Args:
        city (str): City name
    '''
    endpoint = 'http://api.weatherapi.com/v1/current.json'
    key = '07ac51114175472c8ea15758230511'
    temperature, humidity = await call_api(endpoint, key, city)
    if not short:
        return {'Temp': temperature, 'Humidity': humidity}
    return {'Temp': temperature}
