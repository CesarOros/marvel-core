import requests
import json
from datetime import datetime

from search_comics.constants import CHARACTERS


def get_character_comic(endpoint, type_parse):
    response = requests.get(endpoint)
    response_json = json.loads(response.content)
    data = response_json.get("data")
    return parse_data_characters_comics(data, type_parse)


def parse_data_characters_comics(data, type_parse):
    return (
        [
            {
                "id": item.get("id"),
                "name": item.get("name"),
                "image": f'{item.get("thumbnail")["path"]}.{item.get("thumbnail")["extension"]}',
                "appearances": item.get("stories")["returned"],
            }
            for item in data["results"]
        ]
        if type_parse == CHARACTERS
        else [
            {
                "id": item.get("id"),
                "title": item.get("title"),
                "image": f'{item.get("thumbnail")["path"]}.{item.get("thumbnail")["extension"]}',
                "onSaleDate": get_comic_date(item.get("dates")),
            }
            for item in data["results"]
        ]
    )


def get_comic_date(dates) -> str:
    for index in range(len(dates)):
        date = dates[index]
        if date.get("type") == "onsaleDate":
            date_parsed = datetime.strptime(date.get("date"), "%Y-%m-%dT%H:%M:%S-%f")
            return date_parsed.strftime("%Y-%m-%d %H:%M:%S")
    return ""
