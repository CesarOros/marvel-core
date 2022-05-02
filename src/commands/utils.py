from dotenv import load_dotenv
import pymongo
import os

load_dotenv()


def connect_db():
    USER = os.getenv("MONGO_USER")
    PWD = os.getenv("MONGO_PWD")
    client = pymongo.MongoClient(
        f"mongodb+srv://{USER}:{PWD}@marvel.fjb8b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
        uuidRepresentation="standard",
    )
    db = client["marveldb"]
    return db["users"]


def has_word(title, name_comic):
    return False if title.lower().find(name_comic) == -1 else True
