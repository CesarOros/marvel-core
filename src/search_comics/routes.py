from flask import Blueprint, request
from search_comics.constants import AUTHENTICATION_HEADER, URL
from search_comics.constants import SEARCH_TYPE_KEY
from commands.search_comic import get_character_comic
from search_comics.constants import CHARACTERS, COMICS

search_comics = Blueprint("searchComics", __name__)


@search_comics.route("/", methods=["GET"])
def get_comics_characters():
    args = request.args
    criteria = args.get("criteria")
    name_title = args.get("name_title")

    if criteria and name_title:
        endpoint = (
            f"{URL}/{SEARCH_TYPE_KEY[criteria]}{AUTHENTICATION_HEADER}"
            f"&{'name' if SEARCH_TYPE_KEY[criteria] == CHARACTERS else 'title'}={name_title}"
        )
        value_response = CHARACTERS if SEARCH_TYPE_KEY[criteria] == CHARACTERS else COMICS
        response = { value_response : get_character_comic(endpoint, SEARCH_TYPE_KEY[criteria])}

    elif name_title:
        character_endpoint = f"{URL}/{CHARACTERS}{AUTHENTICATION_HEADER}&name={name_title}"
        comics_endpoint = f"{URL}/{COMICS}{AUTHENTICATION_HEADER}&title={name_title}"
        response = {
            "characters": get_character_comic(character_endpoint, CHARACTERS),
            "comics": get_character_comic(comics_endpoint, COMICS),
        }

    else:
        endpoint = f"{URL}/{CHARACTERS}{AUTHENTICATION_HEADER}&orderBy=name"
        response = { 'characters': get_character_comic(endpoint, CHARACTERS)}

    return response
