import uuid
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

def init(cart=None):
    """
    Initializes firestore document for a certain cart
    @param cart: The cart to find the firestore document for, creates a new one if it is None
    @return: A firestore Document object that references the specified cart

    The function returns None if the request couldn't be fulfulled
    """
    cred = credentials.Certificate(
        "../keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json")
    firebase_admin.initialize_app(cred)

    # App is an app object of sorts
    App = firebase_admin.initialize_app(cred, None, 'Cheqout')
    # Client is a firestore client, the docs is https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
    Client = firebase_admin.firestore.client()

    # get a reference to the top level collection
    collection = Client.collection('carts')

    # if cart is not specified, create a new cart
    if cart is None:
        return collection.add({"id": str(uuid.uuid4()), "state": "inactive", "activated": None, "items": []})
    # otherwise, look for the document referencing the cart and return the Document object
    else:
        for document in collection.get():
            if 'id' in document.to_dict() and document.to_dict()['id'] == cart:
                return document.reference
        return None
    
    return None

def activate(cart_document):
    """
    Activates the cart referenced by the document
    @param cart_document: The Document object that represents the specified cart
    @return: a boolean flag representing whether the operation succeeded or not
    """
    field_updates = {'state': 'active', 'activated': str(datetime.datetime.now())}
    cart_document.update(field_updates)
    return True

def deactivate(cart_document):
    """
    Deactivates the cart referenced by the document
    @param cart_document: The Document object that represents the specified cart
    @return: a boolean flag representing whether the operation succeeded or not
    """
    field_updates = {'state': 'inactive', "activated": None}
    cart_document.update(field_updates)
    return True

def add_item(cart_document, item_id):
    """
    Adds an item to the cart referenced by the document
    @param cart_document: The Document object that represents the specified cart
    @item_id: the id of the item being added into the cart
    @return: a boolean flag representing whether the operation succeeded or not
    """
    snapshot = cart_document.get().to_dict()
    print(snapshot)
    item_array = snapshot['items']
    item_found = False
    for item in item_array:
        if item_id == item['id']:
            item_found = True
            item['quantity'] += 1
    if not item_found:
        item_array.append({'id' : item_id, 'quantity' : 1})
    print(snapshot)
    cart_document.set(snapshot)
    return True
