# Import fastapi and create a default test route
import requests
from fastapi import FastAPI

app = FastAPI()


@app.get('/')
async def root():
    '''Returns Hello world for basic testing'''
    return {'message': 'Hello world!!'}


@app.get('/items/{item_id}')
async def read_item(item_id: int, short: bool = True):
    if not short:
        return {'description': short}
    return {'item_id': item_id}


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
