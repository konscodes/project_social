# Import fastapi and create a default test route
from re import template
from fastapi import FastAPI
import fastapi

app = FastAPI()


@app.get('/')
async def root():
    '''Returns Hello world for basic testing'''
    return {'message': 'Hello world!!'}

@app.get('/items/{item_id}')
async def read_item(item_id: int, q: str | None = None, short: bool = True):
    if not short:
        return {'description': short}
    return {'item_id': item_id}

async def call_api(endpoint: str, key: str, city: str):
        temperature, humidity = [0, 1]
        return temperature, humidity

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

## TODO
'''Complete the call api function to send request to weather api and get the data'''