import argparse
import json

from processing.service import build_city_summary

parser = argparse.ArgumentParser(
    description="Скрипт для получения погоды и курса валют"
)
parser.add_argument("--city", type=str, required=True, help="Город для прогноза погоды")
parser.add_argument("--currency", type=str, default="USD", help="Код валюты")
parser.add_argument("--json", action="store_true", help="Вывод в формате JSON")
args = parser.parse_args()

city_summary = build_city_summary(args.city, args.currency)
if args.json:
    print(json.dumps(city_summary))
else:
    print(f"Город: {city_summary['city']}")
    print(
        f"Погода: {city_summary['weather']['temp_c']}°C, {city_summary['weather']['description']}"
    )
    clothes_flag_rus = "да" if city_summary["weather"]["warm_clothes"] else "нет"
    print(f"Тёплая одежда: {clothes_flag_rus}")
    print(
        f"{city_summary['rates']['currency']}→RUB: {city_summary['rates']['rate_to_rub']}"
    )
    expensive_flag_rus = "да" if city_summary["rates"]["expensive"] else "нет"
    print(f"Дорогой курс: {expensive_flag_rus}")
