from src.commands.utils import connect_db
from src.exceptions.exceptions import IncorrectUserPassword
from src.exceptions.exceptions import UserAlreadyExists
import pymongo
import uuid


def get_user(name, password):
    user_collection = connect_db()
    return user_collection.find_one(
        {"name": name, "password": password},
        {"name": 1, "_id": 1, "age": 1, "token": 1},
    )


def get_user_information(name, password):
    try:
        user_result = get_user(name, password)
        if not user_result:
            raise IncorrectUserPassword
        response = {"id": str(user_result["_id"]), **user_result}
        del response["_id"]
    except IncorrectUserPassword:
        response = {"error": "¡Upss!, usuario o contraseña incorrectos"}
    except:
        response = {"error": "Ocurrió un error al intentar obtener el usuario"}

    return response


def insert_user(name, password, age):
    try:
        user_result = get_user(name, password)
        if user_result:
            raise UserAlreadyExists
        user_collection = connect_db()
        user_obj = {
            "name": name,
            "password": password,
            "age": age,
            "token": str(uuid.uuid4()),
        }
        user_inserted = user_collection.insert_one(user_obj)
        del user_obj["_id"]
        del user_obj["password"]
        response = {"id": str(user_inserted.inserted_id), **user_obj}
    except UserAlreadyExists:
        response = {"error": "El usuario ya existe"}
    except:
        response = {"error": "Ocurrió un error al insertar el usuario"}
    return response


def insert_user_comic(name, comic_id):
    user_collection = connect_db()
    user_collection.update_one({"name": name}, {"$push": {"comics": comic_id}})


def get_user_comics(name, password):
    try:
        user_collection = connect_db()
        comics = user_collection.find_one(
            {"name": name, "password": password},
            {"comics": 1, "_id": 0},
        )

        return comics
    except:
        return {"error": "Ocurrió un error al obtener los comics del usuario"}
