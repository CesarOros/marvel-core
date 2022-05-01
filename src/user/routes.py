from flask import Blueprint, request
from commands.users import get_user_information, insert_user
from exceptions.exceptions import IncorrectUserPassword

user = Blueprint("user", __name__)


@user.route("/", methods=["GET"])
def get_users():
    data = request.get_json(force=True)
    name = data.get("name")
    password = data.get("password")
    if not name or not password:
        return {"error": "El parametro name y password deberian estar en el cuerpo"}

    try:
        response = get_user_information(name, password)
    except IncorrectUserPassword:
        response = {"error": "¡Upss!, usuario o contraseña incorrectos"}
    except:
        response = {"error": "Ocurrió un error al intentar obtener el usuario"}

    return response


@user.route("/register", methods=["POST"])
def register_user():
    data = request.get_json(force=True)
    name = data.get("name")
    password = data.get("password")
    age = data.get("age", "")
    if not name or not password:
        return {"error": "El name y password deberian estar en el cuerpo"}

    response = insert_user(name, password, age)
    return response
