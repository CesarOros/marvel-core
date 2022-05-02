from src.exceptions.exceptions import ComicNotFound
from src.constants import CHARACTERS, COMICS
from dotenv import load_dotenv
from datetime import datetime
import requests
import json
import os

load_dotenv()
URL = os.getenv("URL")
AUTHENTICATION_HEADER = os.getenv("AUTHENTICATION_HEADER")


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


def get_comic_by_id(comic_id):
    comic_request = requests.get(f"{URL}/{COMICS}/{comic_id}{AUTHENTICATION_HEADER}")
    comic_response = json.loads(comic_request.content)
    comic = comic_response.get("data")["results"]
    if comic_request.status_code != 200 or not len(comic):
        raise ComicNotFound

    return comic[0]


def get_comics_data(data):
    comics = []
    for comic_id in data.get("comics", []):
        try:
            comic = get_comic_by_id(comic_id)
            comics.append(
                {"title": comic["title"], "date": get_comic_date(comic["dates"])}
            )
        except:
            pass
    return comics
