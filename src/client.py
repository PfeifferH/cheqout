import uuid
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init(key_location="../keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json", cart=None):
    """
    Initializes firestore document for a certain cart
    @param cart: The cart to find the firestore document for, creates a new one if it is None
    @return: A firestore Document object that references the specified cart

    The function returns None if the request couldn't be fulfulled
    """
    cred = credentials.Certificate(
        key_location)
    firebase_admin.initialize_app(cred)

    # App is an app object of sorts
    App = firebase_admin.initialize_app(cred, None, 'Cheqout')
    # Client is a firestore client, the docs is https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
    Client = firebase_admin.firestore.client()

    # get a reference to the top level collection
    collection = Client.collection('carts')

    # if cart is not specified, create a new cart
    if cart is None:
        return collection.add({"state": "inactive", "activated": None, "items": []})[1]
    # otherwise, look for the document referencing the cart and return the Document object
    else:
        for document in collection.get():
            if document.id == cart:
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

def complete(cart_document):
    """
    Completes the cart referenced by the document

    @param cart_document: The Document object that represents the specified cart
    @return: a boolean flag representing whether the operation succeeded or not
    """
    field_updates = {'state': 'completed', "activated": str(datetime.datetime.now())}
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
    item_array = snapshot['items']
    item_found = False
    # if the item already exists in the item list, just add 1 to the quantity
    for item in item_array:
        if item_id == item['id']:
            item_found = True
            item['quantity'] += 1
    # if the item wasn't in the itme list yet, add a new entry to the item list
    if not item_found:
        item_array.append({'id' : item_id, 'quantity' : 1})
    # update the data of the document to match the added item
    cart_document.set(snapshot)
    return True

def remove_item(cart_document, item_id):
    """
    Removes an item to the cart referenced by the document
    @param cart_document: The Document object that represents the specified cart
    @item_id: the id of the item being removed into the cart
    @return: a boolean flag representing whether the operation succeeded or not
    """
    snapshot = cart_document.get().to_dict()
    item_array = snapshot['items']
    # if the item already exists in the item list, just add 1 to the quantity
    for item in item_array:
        if item_id == item['id']:
            # if for some reason there's less than 1 of the item return an error
            if item['quantity'] <= 0:
                return False
            # subtract one item from the quantity
            item['quantity'] -= 1
            # if the new quantity is 0, remove the item from the list
            if item['quantity'] == 0:
                item_array.remove(item)
            cart_document.set(snapshot)
            return True
    # if the item was not found in the list at all, return an error
    return False

def get_items(cart_document):
    """
    Returns a list of all the items in the cart referenced by the document
    @param cart_document: The Document object that represents the specified cart
    @return: A list of objects that represent the items in the cart
    """
    snapshot = cart_document.get().to_dict()
    return snapshot['items']
