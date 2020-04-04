from pymongo import MongoClient
from bson.objectid import ObjectId

client = MongoClient('localhost', 27017)
db = client['whereis_database']


def is_empty():
    return db.locations.count_documents({}) <= 0 or db.items.count_documents({}) <= 0


def fill_test_db():
    location_ids = db.locations.insert_many([{
            "name": "Garage",
            "map": "map1.png"
        },
        {
            "name": "Hangar",
            "map": "map2.png"
        }]).inserted_ids
    db.items.insert_many([{
            "name": "Hammer1",
            "description": "Smashing",
            "image": "hammer.jpg",
            "location": location_ids[0]
        },
        {
            "name": "Hammer2",
            "description": "Smashing",
            "image": "hammer.jpg",
            "location": location_ids[1]
        },
        {
            "name": "Knife1",
            "description": "Sharp",
            "image": "knife.png",
            "location": location_ids[0]
        },
        {
            "name": "Knife2",
            "description": "Sharp",
            "image": "knife.png",
            "location": location_ids[1]
        }])
    print("== Filled test db ==")


def get_locations():
    locations = []
    for location in db.locations.find({}):
        locations.append({
            "id": str(location['_id']),
            "name": location['name'],
            "map": location['map']
        })
    return locations


def get_items(count=None, name=None, location=None):
    items = []
    internal_count = count

    query = {}

    if name:
        query['name'] = name
    if name:
        query['location'] = ObjectId(location)

    for item in db.items.find(query):
        items.append({
            "id": str(item['_id']),
            "name": item['name'],
            "description": item['description'],
            "image": item['image'],
            "location": str(item['location'])
        })
        if count:
            if internal_count > 0:
                internal_count -= 1
            else:
                break

    return items
