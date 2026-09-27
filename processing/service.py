from clients.weather import get_weather
from clients.rates import get_rate
from processing.preprocessing import is_rate_expensive, is_warm_clothes_needed

def build_city_summary(city: str, currency: str = "USD") -> dict[str, any]:
    weather = get_weather(city)
    rate = get_rate(currency)
    
    result = {
        'city': city,
        'weather': {
            **weather,
            'warm_clothes': is_warm_clothes_needed(weather['temp_c'])
        },
        'rates': {
            'currency': currency,
            'rate_to_rub': rate,
            'expensive': is_rate_expensive(rate)
        }
    }
    return result
