from flask import Flask, redirect, request
import requests


from commands.users import get_user, insert_user
from exceptions.exceptions import IncorrectUserPassword
from commands.users import get_user_information
from search_comics.routes import search_comics
from commands.utils import connect_db
from search_comics.constants import AUTHENTICATION_HEADER, COMICS, URL
from commands.users import insert_user_comic
from user.routes import get_users
from user.routes import user
import json

app = Flask(__name__)
app.register_blueprint(search_comics, url_prefix="/searchComics")
app.register_blueprint(user, url_prefix="/users")

PORT = 3200
HOST = "0.0.0.0"

@app.route("/", methods=['POST'])
def home():
    data = request.get_json(force=True)
    name = data.get("name")
    password = data.get("password")
    comic_id = data.get("comic_id")
    if not name or not password:
        return {"error": "El parametro name y password deberian estar en el cuerpo"}
    
    user_request = requests.get(f'http://localhost:{PORT}/users', json={"name": name, 'password': password})
    user_response = json.loads(user_request.content)

    if "error" in user_response:
        return user_response

    if not comic_id:
        return {"error": "Necesitas añadir un comic"}

    comic_request = requests.get(f"{URL}/{COMICS}/{comic_id}{AUTHENTICATION_HEADER}")
    if comic_request.status_code != 200:
        return {"error": "Ocurrió un error al encontrar el comic"}
    
    comic_response = json.loads(comic_request.content)
    insert_user_comic()

    return "hello"

if __name__ == "__main__":
    print(f"Server running in port {PORT}")
    app.run(host=HOST, port=PORT, debug=True)
