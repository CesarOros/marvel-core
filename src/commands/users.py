from urllib import response
import pymongo
import uuid

from exceptions.exceptions import IncorrectUserPassword
from exceptions.exceptions import UserAlreadyExists


def connect_db():
    client = pymongo.MongoClient(
        "mongodb+srv://cesaroros:TUP8QaGCmWiTme3@marvel.fjb8b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
        uuidRepresentation="standard",
    )
    db = client["marveldb"]
    return db["users"]


def get_user(name, password):
    user_collection = connect_db()
    cursor = user_collection.find({"name": name, "password": password})
    return list(cursor)


def get_user_information(name, password):
    user_result = get_user(name, password)
    if not len(user_result):
        raise IncorrectUserPassword
    response = {"id": str(user_result[0]["_id"]), **user_result[0]}
    del response["_id"]
    del response["password"]

    return response


def insert_user(name, password, age):
    user_result = get_user(name, password)

    try:
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
        response = {"error": "el usuario ya existe"}
    except:
        response = {"error": "Ocurrió un error al insertar el usuario"}
    return response

def insert_user_comic():
    user_collection = connect_db()
    user_collection.update_one({'name': 'maritza'},{"$push": {'comics': 998}})
