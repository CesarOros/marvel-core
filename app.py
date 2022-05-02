from src.constants import SEARCH_TYPE_KEY, CHARACTERS, COMICS
from src.exceptions.exceptions import ComicNotFound
from src.commands.utils import has_word
from flask import Flask, request
from flasgger import swag_from, Swagger
from dotenv import load_dotenv
from src.commands.users import (
    get_user_comics,
    get_user_information,
    insert_user_comic,
    insert_user,
)
from src.commands.search_comic import (
    get_character_comic,
    get_comic_by_id,
    get_comics_data,
)
import json
import requests
import os

load_dotenv()
URL = os.getenv("URL")
AUTHENTICATION_HEADER = os.getenv("AUTHENTICATION_HEADER")

PORT = 3200
HOST = "0.0.0.0"

app = Flask(__name__)
swagger = Swagger(app)


@app.route("/searchComics/", methods=["GET"])
@swag_from("./openapi/search_comics.yml")
def search_comics_or_characters():
    args = request.args
    criteria = args.get("criteria")
    name_title = args.get("name_title")

    if criteria and name_title:
        endpoint = (
            f"{URL}/{SEARCH_TYPE_KEY[criteria]}{AUTHENTICATION_HEADER}"
            f"&{'name' if SEARCH_TYPE_KEY[criteria] == CHARACTERS else 'title'}={name_title}"
        )
        value_response = (
            CHARACTERS if SEARCH_TYPE_KEY[criteria] == CHARACTERS else COMICS
        )
        response = {
            value_response: get_character_comic(endpoint, SEARCH_TYPE_KEY[criteria])
        }

    elif name_title:
        character_endpoint = (
            f"{URL}/{CHARACTERS}{AUTHENTICATION_HEADER}&name={name_title}"
        )
        comics_endpoint = f"{URL}/{COMICS}{AUTHENTICATION_HEADER}&title={name_title}"
        response = {
            "characters": get_character_comic(character_endpoint, CHARACTERS),
            "comics": get_character_comic(comics_endpoint, COMICS),
        }

    else:
        endpoint = f"{URL}/{CHARACTERS}{AUTHENTICATION_HEADER}&orderBy=name"
        print(endpoint)
        response = {"characters": get_character_comic(endpoint, CHARACTERS)}

    return response


@app.route("/users/", methods=["GET", "POST"])
@swag_from("./openapi/users.yml")
def get_or_generate_user():
    data = request.get_json(force=True)
    name = data.get("name")
    password = data.get("password")
    age = data.get("age", "")
    if not name or not password:
        return {"error": "Las keys name y password deberian estar en el cuerpo"}
    if request.method == "GET":
        response = get_user_information(name, password)
        print("-----")
    if request.method == "POST":
        response = insert_user(name, password, age)
    return response


@app.route("/addToLayaway/", methods=["POST"])
@swag_from("./openapi/add_layaway.yml")
def add_to_layaway():
    data = request.get_json(force=True)
    name = data.get("name")
    password = data.get("password")
    comic_id = data.get("comic_id")
    if not name or not password:
        return {"error": "El parametro name y password deberian estar en el cuerpo"}

    try:
        user_request = requests.get(
            f"http://localhost:{PORT}/users", json={"name": name, "password": password}
        )
        user_response = json.loads(user_request.content)

        if "error" in user_response:
            return user_response

        if not comic_id:
            return {"error": "Necesitas añadir el id del comic"}
        comic = get_comic_by_id(comic_id)

        insert_user_comic(name, comic_id)

        response = {
            "name": name,
            "comicTitle": comic["title"],
            "message": f"El comic de {name} fue agregado correctamente",
        }
        return response

    except ComicNotFound:
        response = {"error": "¡Upss!, no tenemos registro de este comic"}
    except:
        response = {"error": "Ocurrió un error al agregar el comic"}

    return response


@app.route("/getLayawayList/", methods=["GET"])
@swag_from("./openapi/get_layaway.yml")
def get_layaway_list():
    data = request.get_json(force=True)
    args = request.args
    name = data.get("name")
    password = data.get("password")
    name_comic = args.get("name_comic")
    alph_order = args.get("alph_order")

    if not name or not password:
        return {"error": "El parametro name y password deberian estar en el cuerpo"}

    try:
        user_request = requests.get(
            f"http://localhost:{PORT}/users", json={"name": name, "password": password}
        )
        user_response = json.loads(user_request.content)
        if "error" in user_response:
            return user_response

        comics_response = get_user_comics(name, password)

        if "error" in comics_response:
            return comics_response

        comics = get_comics_data(comics_response)

        if len(comics):
            if name_comic:
                comics = list(
                    filter(
                        lambda item: has_word(item.get("title", ""), name_comic), comics
                    )
                )
            if alph_order:
                comics = sorted(comics, key=lambda item: item["title"])
        return {"comics": comics}

    except:
        return {"error": "Ocurrió un error al obtener los comics"}


if __name__ == "__main__":
    print(f"Server running in port {PORT}")
    app.run(host=HOST, port=PORT, debug=True)
