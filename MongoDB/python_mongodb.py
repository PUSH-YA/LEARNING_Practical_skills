from pymongo import MongoClient
from bson.objectid import ObjectId

mongo_host = "localhost"
mongo_port = 27017
dbname = "trial"
collection_name = "temp"

document = {
    "language": "python"
}

def connect_to_mongodb():
    try:
        client = MongoClient(mongo_host, mongo_port)
        print("Connected to MongoDB successfully!")

        db = client[dbname]

        collection = db[collection_name]
        return collection
    except Exception as e:
        print("failed to connect, ", e)
        return None
    
def insert_doc(collection, document):
    try:
        result = collection.insert_one(document)
        print("Document inserted Succesffully with ID: ", result.inserted_id)
    except Exception as e:
        print("failed to insert ", e)
        
if __name__ == "__main__":
        collection = connect_to_mongodb()
        if collection is not None:
            insert_doc(collection, document)
    


