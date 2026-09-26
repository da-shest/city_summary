from http import get_api_data

BASE_WEATHER_URL = 'https://geocoding-api.open-meteo.com/v1'

WEATHER_CODES = {
	"0": "Clear sky",
	"1": "Mainly clear",
	"2": "Partly cloudy",
	"3": "Overcast",
	"45": "Fog",
	"48": "Depositing rime fog",
	"51": "Light drizzle",
	"53": "Moderate drizzle",
	"55": "Dense drizzle",
	"56": "Light freezing drizzle",
	"57": "Dense freezing drizzle",
	"61": "Slight rain",
	"63": "Moderate rain",
	"65": "Heavy rain",
	"66": "Light freezing rain",
	"67": "Heavy freezing rain",
	"71": "Slight snowfall",
	"73": "Moderate snowfall",
	"75": "Heavy snowfall",
	"77": "Snow grains",
	"80": "Slight rain showers",
	"81": "Moderate rain showers",
	"82": "Violent rain showers",
	"85": "Slight snow showers",
	"86": "Heavy snow showers",
	"95": "Thunderstorm",
	"96": "Thunderstorm with slight hail",
	"97": "Heavy thunderstorm",
	"99": "Thunderstorm with heavy hail"
}

def get_weather(city: str) -> dict:
    city_coordinates = get_city_coordinates(city)
    url = f'{BASE_WEATHER_URL}/forecast'
    params={
            'latitude': city_coordinates['latitude'],
            'longitude': city_coordinates['longitude'],
            'temperature_unit': 'celsius',
            'current': f'{"temperature_2m"},{"weather_code"}'
            }
    data = get_api_data(url, params)
    validate_weather(data)
    result = {
        'temp_c': data['current']['temperature_2m'],
        'description': WEATHER_CODES.get(data['current']['weather_code'], '')
    }
    return result

def validate_weather(data: dict) -> None:
    for field in ('latitude', 'longitude', 'current'):
        if field not in data:
            raise ValueError(f'Отсутствует поле {field}')

    for field in ('time', 'temperature_2m', 'weather_code'):
        if field not in data['current']:
            raise ValueError(f'Отсутствует поле {field} в поле current')

    for field, type in (
        ('latitude', float),
        ('longitude', float),
    ):
        if not isinstance(data[field], type):
            raise TypeError(f'Поле {field} должно иметь тип {type}')

    for field, type in (
            ('time', str),
            ('temperature_2m', float),
            ('weather_code', int),
        ):
            if not isinstance(data['current'][field], type):
                raise TypeError(f'В current поле {field} должно иметь тип {type}')


def get_city_coordinates(city: str) -> dict[str, float]:
    url = f'{BASE_WEATHER_URL}/search'
    params={
            'name': city,
            'count': 1,
            'format': 'json',
            'language': 'en',
            }
    data = get_api_data(url, params)
    validate_coordinates(data)
    result = {
        'latitude': data['results'][0]['latitude'],
        'longitude': data['results'][0]['longitude']
    }
    return result
    


def validate_coordinates(data: dict) -> None:
    if 'results' not in data:
        raise ValueError(f'Отсутствует результат')
    
    for result in data['results']:
        for field in ('id', 'name', 'latitude', 'longitude'):
            if field not in result:
                raise ValueError(f'Отсутствует поле {field}')

        for field, type in (
            ('id', int),
            ('name', str),
            ('latitude', float),
            ('longitude', float),
        ):
            if not isinstance(result[field], type):
                raise TypeError(f'Поле {field} должно иметь тип {type}')
