import uuid

from pymongo import MongoClient, collection

import src.config as config


def get_mongo_collection() -> collection:
    """Connects to MongoDB.

    Function connects to MongoDB cluster in cloud environment in MongoDB Atlas
    using data from config (username, password and cluster).
    Requires creating project and database in it in MongoDB Atlas.

    Returns:
        collection: collection "transcripts" in "Audio-to-text-bot" database.
    """
    username = config.get_settings().mongo_username.get_secret_value()
    password = config.get_settings().mongo_password.get_secret_value()
    cluster = config.get_settings().cluster.get_secret_value()

    uri = f"mongodb+srv://{username}:{password}@{cluster}"
    uri += ".mongodb.net/?retryWrites=true&w=majority"
    client = MongoClient(uri)
    db = client["Audio-to-text-bot"]
    collection = db["transcripts"]
    return collection


def add_document_mongo(path_to_doc: str) -> str:
    """Adds document to MongoDB.

    Function connects to MongoDB via get_mongo_collection.
    Text of file, filename are added to MongoDB collection "transcripts".

    Args:
        path_to_doc (str): path to file.

    Returns:
     - uuid: uuid for added document (stored in MongoDB with document).
    """
    collection = get_mongo_collection()

    with open(path_to_doc, "r") as file:
        text = file.read()
        uid = str(uuid.uuid4())
        doc_to_mongo = {"transcript": text, "uuid": uid}
        collection.insert_one(doc_to_mongo)
    return uid


def get_document_mongo(uid: str) -> dict:
    """Finds document in MongoDB via uuid.

    Args:
        uid (str): uuid of document.

    Returns:
        dict: document from MongoDB with provided uuid.
    """
    collection = get_mongo_collection()
    transcript = collection.find_one({"uuid": uid})
    return transcript
