import uuid
import datetime

import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class CartNotFoundError(Exception):
    """
    An exception for when a specified cart is not found
    """
    pass

class Client():
    """
    A class to represent the client cart

    Provides all functionality needed to interface with the firestore from the client
    """
    def __init__(self, key_location="../keys/cheqout-57ee7-firebase-adminsdk-8b1oa-8dd14d0e11.json", cart=None):
        """
        Initializes firestore document for a certain cart
        @param cart: The cart to find the firestore document for, creates a new one if it is None
        @return: A firestore Document object that references the specified cart

        The function returns None if the request couldn't be fulfulled
        """
        # login to firestore
        cred = credentials.Certificate(
            key_location)
        firebase_admin.initialize_app(cred)

        # App is an app object of sorts
        App = firebase_admin.initialize_app(cred, None, 'Cheqout')
        # Client is a firestore client, the docs is https://googlecloudplatform.github.io/google-cloud-python/latest/firestore/client.html
        client = firebase_admin.firestore.client()

        # assume we can always find the inventory collection
        self.inventory = client.collection('inventory')
        # assume we can always find the users collection
        self.users = client.collection('users')
        # assume we can always find the carts collection
        self.carts = client.collection('carts')
        # assume we can always find the transaction collection
        self.transactions = client.collection('transaction')

        collection = client.collection('carts')
        # if cart is not specified, create a new cart
        if cart is None:
            self.cart = collection.add({"state": "inactive", "activated": None, "items": []})[1]
            return
        # otherwise, look for the document referencing the cart and return the Document object
        else:
            for document in collection.get():
                if document.id == cart:
                    self.cart = document.reference
                    return

        # The code should never run to this point because the cart should have been found
        #   So we throw an exception
        raise CartNotFoundError("Couldn't find cart: " + str(cart))

    def activate(self):
        """
        Activates the cart referenced by the document
        @return: a boolean flag representing whether the operation succeeded or not
        """
        field_updates = {'state': 'active', 'activated': str(datetime.datetime.now())}
        self.cart.update(field_updates)
        return True

    def deactivate(self):
        """
        Deactivates the cart referenced by the document
        @return: a boolean flag representing whether the operation succeeded or not
        """
        field_updates = {'state': 'inactive', "activated": None}
        self.cart.update(field_updates)
        return True

    def complete(self):
        """
        Completes the cart referenced by the document

        @return: a boolean flag representing whether the operation succeeded or not
        """
        field_updates = {'state': 'completed', "activated": str(datetime.datetime.now())}
        self.cart.update(field_updates)
        return True

    def add_item(self, item_id):
        """
        Adds an item to the cart referenced by the document
        @item_id: the id of the item being added into the cart
        @return: a boolean flag representing whether the operation succeeded or not
        """
        snapshot = self.cart.get().to_dict()
        if 'items' not in snapshot:
            snapshot['items'] = []
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
        self.cart.set(snapshot)
        return True

    def remove_item(self, item_id):
        """
        Removes an item to the cart referenced by the document
        @item_id: the id of the item being removed into the cart
        @return: a boolean flag representing whether the operation succeeded or not
        """
        snapshot = self.cart.get().to_dict()
        if 'items' not in snapshot:
            snapshot['items'] = []
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
                self.cart.set(snapshot)
                return True
        # if the item was not found in the list at all, return an error
        return False

    def get_items(self):
        """
        Returns a list of all the items in the cart referenced by the document
        @param cart_document: The Document object that represents the specified cart
        @return: A list of objects that represent the items in the cart
        """
        item_list = []
        snapshot = self.cart.get().to_dict()
        if 'items' not in snapshot:
            return []
        item_snapshot = snapshot['items']
        for item in item_snapshot:
            for document in self.inventory.get():
                if document.id == item['id']:
                    inv_item_dict = document.to_dict()
                    item_data = {'id': item['id'], 'qty': item['quantity']}
                    item_data['name'] = inv_item_dict['name']
                    item_data['price'] = inv_item_dict['price']
                    item_data['tax'] = inv_item_dict['tax']
                    item_data['type'] = inv_item_dict['type']
                    item_list.append(item_data)
        return item_list

    def get_item_data(self, item_id):
        """
        Get the data associated with an item from an inventory
        @param item_id: The id of the item data being requested from
        @return: a dict containing data about the requested item 

        returns none if the item was not found       
        """
        for document in self.inventory.get():
            if document.id == item_id:
                return_data = document.to_dict()
                return_data['id'] = item_id
                return return_data
        return None


    def store_transaction(self, cart_id, user_id):
        """
        Processes and records a transaction from a carts' items
        @param carts: A Collection object representing the carts
        @param transactions: A Collection object representing the transactions
        @param inventory: A Colelction object representing the item inventory
        @param cart_id: The desired cart id to process the transaction with
        @param user_id: The id of the user that is making the transaction
        @return: A Boolean representing whether the transaction succeeded or not
        """
        item_array = None
        # First find the item array from the desired cart
        for document in self.carts.get():
            if document.id == cart_id:
                cart_data = document.to_dict()
                if 'items' in cart_data:
                    item_array = cart_data['items']
        if item_array is None:
            return False
        # Then start populating data for the transaction
        transaction_data = {"user": user_id, "cart": cart_id,
                            "items": [], "subtotal": 0., "tax": 0., "total": 0.}
        for item in item_array:
            # TODO: handle case where item prace wasn't found
            if self.get_item_data(item['id']) is None:
                print("PRICE NOT FOUND")
            else:
                item_data = self.get_item_data(item['id'])
                transaction_data['subtotal'] += float(
                    item_data['price']) * item['quantity']
                # Add tax if the item is taxable
                if float(item_data['tax']) == 1:
                    transaction_data['tax'] += float(
                        item_data['price']) * item['quantity'] * 0.13
                # process the item as a countable item
                if item_data['format'] == "0":
                    transaction_data['items'].append(
                        {'id': item['id'], 'name': item_data['name'], 'qty': item['quantity'], 'unit_price': item_data['unit_price']})
                # process the item as a weighted item
                if item_data['format'] == "1":
                    transaction_data['items'].append(
                        {'id': item['id'], 'name': item_data['name'], 'weight': item['quantity'], 'unit_price': item_data['unit_price']})
        transaction_data['total'] = transaction_data['subtotal'] + \
            transaction_data['tax']
        # Add a timestamp
        transaction_data['timestamp'] = datetime.datetime.utcnow().strftime(
            '%B %d, %Y, %H:%M:%S UTC').lstrip("0").replace(" 0", " ")
        # TODO: find ways to implement this data
        transaction_data['auth_code'] = 'TEST AUTH CODE'
        transaction_data['payment_type'] = -1
        self.transactions.add(transaction_data)
        print(transaction_data)
