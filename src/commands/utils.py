import pymongo

def connect_db():
    client = pymongo.MongoClient(
        "mongodb+srv://cesaroros:TUP8QaGCmWiTme3@marvel.fjb8b.mongodb.net/myFirstDatabase?retryWrites=true&w=majority",
        uuidRepresentation="standard",
    )
    db = client["marveldb"]
    return db["users"]