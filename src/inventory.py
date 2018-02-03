import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init(key="../keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json"):
    """
    Initializes firestore
    @return: returns a Collection Object that references the top level inventory collection in Firestore
    """
    cred = credentials.Certificate(
        key)
    firebase_admin.initialize_app(cred)

    # App is an app object of sorts
    App = firebase_admin.initialize_app(cred, None, 'Cheqout Inventory')
    # Client is a firestore client, the docs is https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
    Client = firebase_admin.firestore.client()

    # get a reference to the top level collection
    return Client.collection('inventory')

def get_item_data(inventory, item_id):
    """
    Get the data associated with an item from an inventory
    @param inventory: The Collection object that represents the inventory
    @param item_id: The id of the item data being requested from
    @return: a dict containing data about the requested item
    """
    for document in inventory.get():
        if document.id == item_id:
            return_data = document.to_dict()
            return_data['id'] = item_id
            return return_data
    return None

def add_item_data(inventory, item_id, item_data):
    """
    Stores the item data and item id to the firestore database
    @param inventory: The Collection object that represents the inventory
    @param item_id: The id of the item data being stored in
    @param item_data: The data of the item to be stored
    @return: A boolean flag representing whether the operation succeeded or not

    Assumes the input item_data is valid
    """
    # if the item already exists, just update its' information
    for document in inventory.get():
        if document.id == item_id:
            doc_ref = document.reference
            doc_ref.set(item_data)
            return True
    # otherwise, create a new entry and add it to the collection
    inventory.add(item_data, item_id)
    return True